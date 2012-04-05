from csbot.core import Plugin, command

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
# - make persistent, ideally with a better backend than just strings, e.g. pickle
# - auto expansion!

class Abbreviations(Plugin):
    DATA = 'dictionary'
    USAGE_ADD = "Usage: !abbr.add TLA \"Three Letter Acronym\""
    USAGE_EDIT = "Usage: !abbr.edit TLA \"Three Letter Abbreviation\""
    USAGE_ABBR = "Usage: !abbr TLA"
    USAGE_REM = "Usage: !abbr.rem TLA"

    abbrs = {}

    def setup(self):
        # TODO: store persistent dictionary in db
        pass
#        try:
#            abbrs = self.get(self.DATA)
#        except:
#            self.set(self.DATA, {})

    @command('abbr.add')
    def add_command(self, event):
        if len(event.data) < 2:
            if len(event.data) < 1:
                event.error("I can't add an empty abbreviation!")
            else:
                event.error("You need to define the expansion for '%s'" % event.data[0])

            event.reply(self.USAGE_ADD, True)
            return

        #abbrs = self.get(self.DATA)
        abbreviation = event.data[0]
        expansion = event.data[1]

        if abbreviation in self.abbrs:
            event.error("I already have an expansion, '%s' = '%s'. Try the edit command." % (abbreviation, self.abbrs[abbreviation]))
            event.reply(self.USAGE_EDIT, True)
        else:
            self.abbrs[abbreviation] = event.data[1]
#            self.set(self.DATA, self.abbrs)
            event.reply("Added '%s' = '%s'." % (abbreviation, expansion))


    @command('abbr.edit')
    def edit_command(self, event):
        if len(event.data) < 2:
            if len(event.data) < 1:
                event.error("I can't edit nothing!")
            else:
                event.error("You need to define a new expansion for '%s'" % event.data[0])

            event.reply(self.USAGE_EDIT, True)
            return

        abbreviation = event.data[0]
        if abbreviation not in self.abbrs:
            event.error("I don't have an abbreviation for '%s'.  Try the add command instead." % abbreviation)
            event.reply(self.USAGE_ADD, True)
        else:
            prev = self.abbrs[abbreviation]
            self.abbrs[abbreviation] = event.data[1]
            event.reply("Changed abbreviation for '%s' from '%s' to '%s'." % (abbreviation, prev, event.data[1]))

    @command('abbr')
    def abbr_command(self, event):
        if len(event.data) < 1:
            event.error("You need to give me an abbreviation to expand!")
            event.reply(USAGE_ABBR, True)
            return

        abbreviation = event.data[0]
        if abbreviation not in self.abbrs:
            event.error("I don't have an abbreviation for '%s'.  Ask someone to !abbr.add one." % abbreviation)
        else:
            event.reply("'%s' = '%s'.  If this abbreviation is wrong, !abbr.edit it." % (abbreviation, self.abbrs[abbreviation]))

    @command('abbr.rem')
    def rem_command(self, event):
        if len(event.data) < 1:
            event.error("You need to give me an abbreviation to remove!")
            event.reply(USAGE_REM, True)
            return

        abbreviation = event.data[0]
        if abbreviation not in self.abbrs:
            event.reply("'%s' was not in my list anyway." % abbreviation)
        else:
            prev = self.abbrs[abbreviation]
            del self.abbrs[abbreviation]
            event.reply("Removed the abbreviation '%s' = '%s'" % (abbreviation, prev))

        

