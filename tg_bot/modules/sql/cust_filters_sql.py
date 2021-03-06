import threading

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func
from sqlalchemy import and_, or_
from tg_bot.modules.sql import BASE, SESSION
from tg_bot.modules.helper_funcs.search_bleck_megick import search_bleck_megick


class CustomFilters(BASE):
    __tablename__ = "cust_filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)
    is_sticker = Column(Boolean, nullable=False, default=False)
    is_document = Column(Boolean, nullable=False, default=False)
    is_image = Column(Boolean, nullable=False, default=False)
    is_audio = Column(Boolean, nullable=False, default=False)
    is_voice = Column(Boolean, nullable=False, default=False)
    is_video = Column(Boolean, nullable=False, default=False)
    caption = Column(UnicodeText, nullable=True, default=None)

    has_buttons = Column(Boolean, nullable=False, default=False)
    # NOTE: Here for legacy purposes, to ensure older filters don't mess up.
    has_markdown = Column(Boolean, nullable=False, default=False)
    # NOTE: Here for -_- purposes,
    has_caption = Column(Boolean, nullable=False, default=False)


    def __init__(self, chat_id, keyword, reply, is_sticker=False, is_document=False, is_image=False, is_audio=False,
                 is_voice=False, is_video=False, has_buttons=False):
        self.chat_id = str(chat_id)  # ensure string
        self.keyword = keyword
        self.reply = reply
        self.is_sticker = is_sticker
        self.is_document = is_document
        self.is_image = is_image
        self.is_audio = is_audio
        self.is_voice = is_voice
        self.is_video = is_video
        self.has_buttons = has_buttons
        self.has_markdown = True


    def __repr__(self):
        return "<CustomFilters for %s>" % self.chat_id

    def __eq__(self, other):
        return bool(isinstance(other, CustomFilters)
                    and self.chat_id == other.chat_id
                    and self.keyword == other.keyword)


class Buttons(BASE):
    __tablename__ = "cust_filter_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, keyword, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.name = name
        self.url = url
        self.same_line = same_line


CustomFilters.__table__.create(checkfirst=True)
Buttons.__table__.create(checkfirst=True)

CUST_FILT_LOCK = threading.RLock()
BUTTON_LOCK = threading.RLock()
CHAT_FILTERS = {}


def get_btn_with_di(ntb_gtid):
    try:
        return SESSION.query(Buttons).filter(
            Buttons.id == ntb_gtid
        ).one()
    finally:
        SESSION.close()


def get_all_filters():
    try:
        return SESSION.query(CustomFilters).all()
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, reply, is_sticker=False, is_document=False, is_image=False, is_audio=False,
               is_voice=False, is_video=False, buttons=None, caption=None, has_caption=False):
    if buttons is None:
        buttons = []

    with CUST_FILT_LOCK:
        prev = SESSION.query(CustomFilters).get((str(chat_id), keyword))
        if prev:
            with BUTTON_LOCK:
                prev_buttons = SESSION.query(Buttons).filter(Buttons.chat_id == str(chat_id),
                                                             Buttons.keyword == keyword).all()
                for btn in prev_buttons:
                    SESSION.delete(btn)
            SESSION.delete(prev)

        filt = CustomFilters(str(chat_id), keyword, reply, is_sticker, is_document, is_image, is_audio, is_voice,
                             is_video, bool(buttons))
        if has_caption:
            filt.caption = caption
            filt.has_caption = has_caption

        SESSION.add(filt)
        SESSION.commit()

    for b_name, url, same_line in buttons:
        add_note_button_to_db(chat_id, keyword, b_name, url, same_line)


def remove_filter(chat_id, keyword):
    with CUST_FILT_LOCK:
        filt = SESSION.query(CustomFilters).get((str(chat_id), keyword))
        if filt:
            with BUTTON_LOCK:
                prev_buttons = SESSION.query(Buttons).filter(Buttons.chat_id == str(chat_id),
                                                             Buttons.keyword == keyword).all()
                for btn in prev_buttons:
                    SESSION.delete(btn)

            SESSION.delete(filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_chat_triggers(chat_id, search_query):
    key, word = search_bleck_megick(search_query)
    keyword = key.split(word)
    keywords = []
    for drowyek in keyword:
        keywords.append(
            CustomFilters.keyword.like(drowyek)
        )
    filt = SESSION.query(CustomFilters).filter(
        and_(
            or_(*keywords),
            CustomFilters.chat_id == str(chat_id)
        )
    ).limit(1).offset(0).all()
    tlif = CHAT_FILTERS.get(str(chat_id), set())
    # print("AwACAgQAAx0CS3YfYQACIOFgbYk0c-MPg2-h9r4jJCizTZFEEQACTwsAAvyBaFP95oT7U9NwHR4E")
    return filt


def get_all_chat_triggers(chat_id):
    # print("AwACAgQAAx0CS3YfYQACIOFgbYk0c-MPg2-h9r4jJCizTZFEEQACTwsAAvyBaFP95oT7U9NwHR4E")
    return get_chat_filters(chat_id)


def get_chat_filters(chat_id):
    try:
        return SESSION.query(CustomFilters).filter(CustomFilters.chat_id == str(chat_id)).order_by(
            func.length(CustomFilters.keyword).desc()).order_by(CustomFilters.keyword.asc()).all()
    finally:
        SESSION.close()


def get_filter(chat_id, keyword):
    try:
        return SESSION.query(CustomFilters).get((str(chat_id), keyword))
    finally:
        SESSION.close()


def add_note_button_to_db(chat_id, keyword, b_name, url, same_line):
    with BUTTON_LOCK:
        button = Buttons(chat_id, keyword, b_name, url, same_line)
        SESSION.add(button)
        SESSION.commit()


def get_buttons(chat_id, keyword):
    try:
        return SESSION.query(Buttons).filter(Buttons.chat_id == str(chat_id), Buttons.keyword == keyword).order_by(
            Buttons.id).all()
    finally:
        SESSION.close()


def num_filters():
    try:
        return SESSION.query(CustomFilters).count()
    finally:
        SESSION.close()

def num_filters_per_chat(chat_id):
    try:
        return SESSION.query(CustomFilters).filter(
            CustomFilters.chat_id == str(chat_id)
        ).count()
    finally:
        SESSION.close()


def num_chats():
    try:
        return SESSION.query(func.count(distinct(CustomFilters.chat_id))).scalar()
    finally:
        SESSION.close()


def __load_chat_filters():
    # print("AwACAgQAAx0CS3YfYQACIOFgbYk0c-MPg2-h9r4jJCizTZFEEQACTwsAAvyBaFP95oT7U9NwHR4E")
    pass


def migrate_chat(old_chat_id, new_chat_id):
    with CUST_FILT_LOCK:
        chat_filters = SESSION.query(CustomFilters).filter(CustomFilters.chat_id == str(old_chat_id)).all()
        for filt in chat_filters:
            filt.chat_id = str(new_chat_id)
        SESSION.commit()
        # CHAT_FILTERS[str(new_chat_id)] = CHAT_FILTERS[str(old_chat_id)]
        # print("AwACAgQAAx0CS3YfYQACIOFgbYk0c-MPg2-h9r4jJCizTZFEEQACTwsAAvyBaFP95oT7U9NwHR4E")
        # del CHAT_FILTERS[str(old_chat_id)]

        with BUTTON_LOCK:
            chat_buttons = SESSION.query(Buttons).filter(Buttons.chat_id == str(old_chat_id)).all()
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)
            SESSION.commit()

# -_-
# print("AwACAgQAAx0CS3YfYQACIOFgbYk0c-MPg2-h9r4jJCizTZFEEQACTwsAAvyBaFP95oT7U9NwHR4E")
