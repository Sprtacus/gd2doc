# A script demonstrating full parsing.
# Contains multiple features.
# TODO: top header todo

extends Node2D
class_name FullExample

# Emitted when something happens
signal something(value)

# Example action enum
enum Action { RUN, JUMP = 3, CROUCH }

# Important constant
const PI = 3.14
# TODO: constant to check

# The player's score
var score: int = 0

# Called every frame
func _process(delta: float) -> void:
    pass

# Adds a value to score
func add(value: int = 1) -> int:
    score += value
    return score

# TODO: final todo
