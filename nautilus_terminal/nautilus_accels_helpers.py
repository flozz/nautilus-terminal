from . import logger


NAUTILUS_ACCELS_BACKUP = {}  # {"action_prefix.action_name": ["accel"], ...}


def backup_nautilus_accels(nautilus_app, nautilus_window):
    if NAUTILUS_ACCELS_BACKUP:
        return

    logger.log("backup_nautilus_accels: backuping accels...")

    # app
    for action in ["app.%s" % a for a in nautilus_app.list_actions()]:
        NAUTILUS_ACCELS_BACKUP[action] = nautilus_app.get_accels_for_action(
            action
        )

    # win, slot, view,...
    for action_prefix in nautilus_window.list_action_prefixes():
        # Skip Nautilus Terminal actions
        if action_prefix.startswith("nterm"):
            continue
        for action in [
            "%s.%s" % (action_prefix, a)
            for a in nautilus_window.get_action_group(
                action_prefix
            ).list_actions()
        ]:
            NAUTILUS_ACCELS_BACKUP[action] = (
                nautilus_app.get_accels_for_action(action)
            )

    # row
    # TODO get accels from the "row" group (nautilus side bar)


def remove_nautilus_accels(nautilus_app):
    if not NAUTILUS_ACCELS_BACKUP:
        logger.error(
            "remove_nautilus_accels: Accels will not be removed: accels have not been backuped"
        )
        return
    logger.log("remove_nautilus_accels: removing accels...")
    for action in NAUTILUS_ACCELS_BACKUP:
        nautilus_app.set_accels_for_action(action, [])


def restore_nautilus_accels(nautilus_app):
    if not NAUTILUS_ACCELS_BACKUP:
        logger.error(
            "remove_nautilus_accels: Accels cannot be restored: accels have not been backuped"
        )
        return
    logger.log("restore_nautilus_accels: restoring accels...")
    for action, accels in NAUTILUS_ACCELS_BACKUP.items():
        nautilus_app.set_accels_for_action(action, accels)
