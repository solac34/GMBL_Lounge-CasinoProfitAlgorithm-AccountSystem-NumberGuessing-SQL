# GMBL Lounge Project
Gambling never been this easy: just guess the number, and lose!


## The Game
Guess the number.
User chooses an interval to guess, as the interval increases, the prize increases too!.
Guess in 1-10 range for 2x.
Guess in 1-50 range for 5x.
Guess in 1-100 range for 15x.
Guess in 1-300 range for 50x.
Guess in 1-500 range for 100x.
Guess in 1-1000 range for 1000x.

Uses recursive function to playing the game, after logging in has completed.

## About the Algorithm
There are 2 algorithms (not complicated to call it an algorithm) which as follows: Pool and Limit.
### Pool Algorithm
Set the pool as desired,(e.g. 15000$) As the guests gamble, they will lose until the pool profits 15000$. If user will gain less than 1% of the pool's desired profit, let user win, even if the pool is not full yet.After the pool reaches the expected value, guests can win as long as their prize won't pool go under the expected value.
### Limit Algorithm
Set a play count to profit after this much of games played.(e.g. 100). If the guest's prize is higher than the last games'(resets after each 100 games) profits, user loses.In opoosite condition, user will have 4x chance to win.

## Features
<ul> 
<li>Prompt-Based Gambling(no real money had ever been used!!)</li>
<li>Create an account to start with 100 balance.</li>
<li>Uses SQL to keep track of any data you can imagine.</li>
<li>Use admin panel to make unbelievable profits, to reset the pool or see some data.</li>

</ul>

### Sign Up Features
<ul>
<li>Some length restrictions for email and password.</li>
<li>Password must contain an uppercase letter, a lowercase letter and a number.</li>
<li>Email must contain .com at the end and '@' mark by  complying the condition:. Not being in the first 3 characters.</li>
<li>Email verification via yagmail. No email-password supplied in resource file.</li>
</ul>

### Admin Panel Features
<ul>
<li>Uses match-case to run commands.</li>
<li>See total profits ever made by entering "profit sum"</li>
<li>See the max profit ever made by entering "max profit"</li>
<li>See the min profit ever made by entering "profit sum"</li>
<li> Set the data limit for limit algorithm by entering "set data limit"</li>
<li>Set the profit multiplier by entering "set profit multiplier"</li>
<li>Set the profit mode to pool or limit by entering "set profit mode"</li>
<li>Set the pool profit by entering "set pool profit"</li>
<li>Reset the pool's current earnings to collect more money.You can think of this as withdrawing the money, by entering "reset pool"</li>
</ul>