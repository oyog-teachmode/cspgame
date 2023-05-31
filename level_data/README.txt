this is the info for the tile loader.

each file has three lists

THE FIRST LIST:
the list contains several numbers per row. the number used is tile to use from the tileset. 
the game will automatically decide what properties a tile has based off of its number.


THE SECOND LIST:
the collision map. (Also contains starting position for the PLAYER [represented by "P"])
rather than number its a single string per row
"X" represents a tile with collision all around. can be represented as a simple box
a space represents no collision

IDEA: other types of collision could be added

wedge collision:
"Q" \|

"V" |/

"M" /|

"I" |\

best used for when you have a diagonal wall


THE THIRD LIST:
lists the position of NPCs 
its formatted a little differently from the rest of the lists.
