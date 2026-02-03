# endgame-phase-1

So you know how the first part of the end of the Marvel Universe was in multiple stages?

This be like that.

This assignment will cover duties 5,6,11, and 12

In the TDD pyramid, you built an app tracking your progress on the themes and relevant duties.
Now, you'll build out an API backend to capable of storing and updating you theme progress.

## PASS CRITERIA
- Strong evidence of clean code principles and TDD (non-negotiable)

- Coins
    - Each Coin needs to have a unique non-integer ID (why is that?)
    - The table needs to conform to 2NF (minimal duplication)

- There is an API availble to access the Coins
    - It should be possible to add, update, remove Coins
    - A Coin should be connected to a one or more Duties which is connected to one or more KSBs.
    - You will need to demonstrate validation-for example, should you be able to have duplicate
    Coins? What makes a Coin the same as another?
    - Endpoints should reflect solid API practices (it should be possible to hit /coins with a GET
    request to return back themese)

- The API will need to be deployable via pipeline. Be prepare to demonstrate this if a change is
required.

## MERIT CRITERIA
You want to create a new endpoint so that /duties/D7 will get you the list of themes that include D7. In
addition, /ksb/K1 will return all the duties that contain K1. However, you
want to ensure that your previous
endpoints still work. How can you make this possible?

Testing CI again!