from collections import defaultdict
from time import time

from flask import current_app

from app import db
from models import Certification, Education, Experience, Project, Settings, Skill


def _cache_bucket():
    return current_app.extensions.setdefault('site_cache', {})


def _get_cached(key, ttl_seconds, loader):
    bucket = _cache_bucket()
    cached = bucket.get(key)
    now = time()

    if cached and now - cached['timestamp'] < ttl_seconds:
        return cached['value']

    value = loader()
    bucket[key] = {'timestamp': now, 'value': value}
    return value


def clear_site_cache():
    _cache_bucket().clear()


def _detach(items):
    if items is None:
        return None

    if isinstance(items, list):
        for item in items:
            db.session.expunge(item)
        return items

    db.session.expunge(items)
    return items


def get_settings_cached(ttl_seconds=30):
    def load():
        settings = Settings.query.first()
        return _detach(settings) if settings else None

    return _get_cached('settings', ttl_seconds, load)


def get_unread_message_count(ttl_seconds=15):
    from models import Message

    return _get_cached(
        'unread_message_count',
        ttl_seconds,
        lambda: Message.query.filter_by(is_read=False).count(),
    )


def get_resume_payload(ttl_seconds=30):
    def load():
        skills = _detach(Skill.query.order_by(Skill.display_order).all())
        grouped_skills = defaultdict(list)
        for skill in skills:
            grouped_skills[skill.category].append(skill)

        return {
            'settings': get_settings_cached(ttl_seconds),
            'skills_by_category': dict(grouped_skills),
            'education_list': _detach(Education.query.order_by(Education.display_order).all()),
            'experience_list': _detach(Experience.query.order_by(Experience.display_order).all()),
            'cert_list': _detach(Certification.query.order_by(Certification.display_order).all()),
            'projects_list': _detach(Project.query.order_by(Project.created_at.desc()).all()),
        }

    return _get_cached('resume_payload', ttl_seconds, load)
