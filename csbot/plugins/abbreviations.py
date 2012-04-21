from csbot.core import Plugin, PluginFeatures

# Abbreviations plugin
# !abbr.add
# !abbr RDQ
# dictionary, abbreviation to full text + timestamp
# if auto enabled
#   then timestamp first occurence of expanding
#   next time, if timestamp more than tolerance, expand + set new timestamp
#   else ignore
#
# config:
# bool auto
# int delay/frequency/tolerance value
#
# commands:
# add
# expand
# toggle/set auto
# set delay freq
# poss some kind of mass add option if scrapable from anywhere

# TODO:
# - auto expansion!


class Abbreviations(Plugin):
    features = PluginFeatures()

    DATA = 'dictionary'
    # TODO: change usage text to use user input?
    USAGE_ADD = "Usage: !abbr.add TLA \"Three Letter Acronym\""
    USAGE_EDIT = "Usage: !abbr.edit TLA \"Three Letter Abbreviation\""
    USAGE_ABBR = "Usage: !abbr TLA"
    USAGE_REM = "Usage: !abbr.rem TLA"

    def setup(self):
        pass

    def teardown(self):
        pass

    # TODO:
    # use remaining event data rather than event data [1]?
    #   > abbr.add TLA Three Letter Acronym
    # or: keep as is; allows more expansion
    #   e.g. general 'facts' plugin with short, expansion + link
    @features.command('abbr.add')
    def add_command(self, event):
        if len(event.data) < 2:
            if len(event.data) < 1:
                event.error("I can't add an empty abbreviation!")
            else:
                event.error("You need to define the expansion for '{}'"
                        .format(event.data[0]))

            event.reply(self.USAGE_ADD, True)
            return

        abbreviation = event.data[0]
        expansion = event.data[1]
        current = self.db.abbrs.find_one({"abbreviation": abbreviation})

        if current is not None:
            event.error("I already have an expansion, '{}' = '{}'. \
                    Try the abbr.edit command."
                    .format(abbreviation, current["expansion"]))
            event.reply(self.USAGE_EDIT, True)
        else:
            self.db.abbrs.insert({
                "abbreviation": abbreviation,
                "expansion": expansion})
            event.reply("Added '{}' = '{}'.".format(abbreviation, expansion))

    @features.command('abbr.edit')
    def edit_command(self, event):
        if len(event.data) < 2:
            if len(event.data) < 1:
                event.error("I can't edit nothing!")
            else:
                event.error("You need to define a new expansion for '{}'"
                        .format(event.data[0]))

            event.reply(self.USAGE_EDIT, True)
            return

        abbreviation = event.data[0]
        expansion = event.data[1]
        current = self.db.abbrs.find_one({"abbreviation": abbreviation})

        if current is None:
            event.error("I don't have an abbreviation for '{}'.  Try the \
                    abbr.add command instead.".format(abbreviation))
            event.reply(self.USAGE_ADD, True)
        else:
            self.db.abbrs.update(
                    {"abbreviation": abbreviation},
                    {"$set": {"expansion": expansion}})
            event.reply("Changed abbreviation for '{}' from '{}' to '{}'."
                    .format(abbreviation, current["expansion"], expansion))

    @features.command('abbr')
    def abbr_command(self, event):
        if len(event.data) < 1:
            event.error("You need to give me an abbreviation to expand!")
            event.reply(self.USAGE_ABBR, True)
            return

        abbreviation = event.data[0]
        current = self.db.abbrs.find_one({"abbreviation": abbreviation})

        if current is None:
            event.error("I don't have an abbreviation for '{}'.  \
                    Ask someone to abbr.add one.".format(abbreviation))
        else:
            event.reply("'{}' = '{}'.  If this abbreviation is wrong, \
                    abbr.edit it.".format(abbreviation, current["expansion"]))

    @features.command('abbr.rem')
    @features.command('abbr.del')
    def rem_command(self, event):
        if len(event.data) < 1:
            event.error("You need to give me an abbreviation to remove!")
            event.reply(self.USAGE_REM, True)
            return

        abbreviation = event.data[0]
        current = self.db.abbrs.find_one({"abbreviation": abbreviation})

        if current is None:
            event.reply("'{}' was not in my list anyway.".format(abbreviation))
        else:
            self.db.abbrs.remove({"abbreviation": abbreviation})
            event.reply("Removed the abbreviation '{}' = '{}'"
                    .format(abbreviation, current["expansion"]))
