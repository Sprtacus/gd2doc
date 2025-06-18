# Example script
# Used for parser tests.

extends Node
class_name Example

# Signal emitted when done
signal done(value)

# Test enum
enum State { IDLE, RUNNING = 2 }

# Max speed
const MAX_SPEED = 10

# Character name
var name: String = "Bob"

# Called when ready
func _ready():
    pass

# Say greeting
func greet(to: String = "World") -> String:
    return "Hello, %s" % to

# TODO: add more
