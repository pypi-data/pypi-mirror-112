dir utils/core
types [a dictionary for add commands which would set the config file]
decks
bindings
dir cards
dir parent_notes

A card file will have the following:
schedule
tags
config
- reviewer
- editor
- parent_note

it may have some auxfiles. e.g.
basic
-(frontimage)
-(backimage)
-(frontaudio)
-(backaudio)
-front
-back
latex
-front.latex
-back.latex

Example:
a latex card would use the default reviewer (and supply all the required auxfiles for that); have no parent note; but use an editor to edit the two latex auxfiles and convert them to images on close. It would override f and b to edit the front and back latex respectively.

Example: 
image occlusion also use the default reviewer, but have no aux files. It would link to a parent note and use a custom editor that would open the parent_note (which can be configured however) for editing, probably in a separate window.

Example:
A type the answer question would not need a parent note, but it would use a custom editor to edit the type field(s) and it would use a custom reviewer to ask for user input.
a simple mode var
- home / add / review
- (edit is a subclass of add)
- (preview is a subclass of edit)

If a then vinka hands controls entirely over to the basic editor until receiving control back
If r likewise to the reviewer.
The previewer is presented with a list of the editor's shortcuts and asked to honor them.
The editor is responsible for initializing the card's files (using an id and timestamp provided by vinka)

reload conditions
- after add
- after edit
- on load

vinka will show a list of decks but it only handles very basic things like changes between cards.

vinka is designed to be entirely modular so that any part can be edited or replaced. A CARD is the source of authority. It decides what editor edits it, what reviewer reviews it, and what scheduler schedules it. The browser can be changed at will.

The browser may save quite a bit of extra data to try to speed up and facilitate its operations, but the cards ultimately determine this. They are self contained: they specify their servants, their history, and their due date. This is true even when multiple cards correspond to a single note e.g. image occlusion. The cards specify their parent note which is stil conceived of as subservient.

4 strengths
-----------
browsing - visual mode
statistics - 8 lines of unicode blocks
reviewing  - very customizable
opening    - last command with different arg; tab completion; BASH ALIASES 
CLI
-vD                        visual decks
-vq {PATTERN}              visual search
-a  [DECK]                 add a single card of type determined by deck
-A  [DECK]                 add multiple cards
-o  [DECK]                 add image occlusion card
-q  {pattern} [DECK]       list cids of all matches
-s  [DECK]                 study
-S  [DECK]                 statistics
-D                         lists decks (and asks?) if no arg
-e  [DECK/CID]             edit the decks file # edit the decks file if no argument given
-b  {dest} [DECK]          backs up all card files to dest
-B  {dest}                 backs up an entire copy of the system to dest (reviewers, editors, &c)
-h, --help                 print this help page
-c  {CID}                  run the command on the specified card (will ignore deck argument)
-d  {DECK}                 operate on the specified deck
-x  {DECK/CID}
--date {date}              operate on the cards due on date; reviews will be dated today
--simulate-date            operate on the cards due on date; reviews will be dated as simulated-date
--import {source}          import cards; resolve conflicts (there are none it is just concatenation)
--filter  [FILE]           specifiy or create a filter file
-                          other commands may be added by the user
-                          card creation commands will work here and in creation mode

VISUAL DECK
- j   move down one deck
- k   move up one deck
- a   add one note with type basic
- A   add several notes
- o   (add one note with image occlusion)
- s   study the current deck
- S   show statistics for the current deck
- r   rename the current deck
- +   create a new deck
- x   delete the current deck
- q   run a search on the selected deck

VISUAL SEARCH 
- q   exit visual search
- j   go down one entry
- k   go up one entry
- spc preview entry
- ent preview entry
- x   delete card
- e   edit card


REVIEW (for basic reviewer)

     |  cont  |   no
-----|--------|--------
save |  enter |   
-----|--------|--------
no   |   x    |  q,esc
-----|--------|--------

go back in review
-h,u    no history change, see prev card
go back in preview
-u      delete current card, see prev card
-h      make current card, see prev card

(there is no going forward)

-     should restore the terminal after use
- e   enter editing the front side
- f   enter editing the front side (must be implemented)
- b   enter editing for the back side (must be implemented)
- t   enter editing for the tags (at bottom; may be overriden by reviewer)
- x   delete card --> y/n
- spc move to backside / mark as good
- ent move to backside / mark as good
- 1   mark as again
- 2   mark as hard
- 3   mark as good
- 4   mark as easy
- esc return to home / deck menu
- @   suspend card
- -   bury card
- *   mark card (!r for mark with red)
- if  specify path to front img file in command bar - refresh review
----  the editor (which is executing this operation also has the privelege of changing the config / note type)
- ib  specify path to back  img file in command bar - refresh review
- ic  specify path to cntxt img file in command bar - refresh review
- vf  specify path to front img file as clipboard - refresh review
- vb  specify path to back  img file as clipboard - refresh review
- vc  specify path to cntxt img file as clipboard - refresh review
- H   go back one card and undo scheduling changes
- u   go back one card and undo scheduling changes
- p   play audio

PREVIEW (for viewing cards while in add mode)
- inherits cmds from REVIEW
- disinherits grading cmds
- many commands like for vb start the editor and pass it an argument
- w   create the card and open another (of the same type)
- ent create the card and open another (of the same type)
- q   discard (delete) the card without saving and return to home
- x   create the card and return to home
- H   edit the most recent card (can be repeated to go farther back)
- o   create image occlusion; key-bindings to types should not interfere

EDIT (for basic editor)
- this *is* vim but with option -u custom.vimrc
- --> for such things as tab autocompletion
- vim starts in insert mode
- <tab> move between front and back splits
- <enter> same as write & quit -> this will take the user to the editor shell which will transfer the user to preview.
I will use SQL for cacheing because this is a dispensable way of doing things.
