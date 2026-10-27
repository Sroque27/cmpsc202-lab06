"""
Lab 06: Demystifying Dynamic Programming with Coin Change

This file implements three approaches for solving the minimum
coin change problem and compares their performance.
"""

import time

import matplotlib.pyplot as plt


def coin_change_recursive(coins, amount):
    """
    Find the minimum number of coins using naive recursion.

    Parameters
    ----------
    coins : list[int]
        The available coin denominations.

    amount : int
        The target amount.

    Returns
    -------
    int
        The minimum number of coins needed, or -1 if exact change
        cannot be made.
    """

    # No coins are needed to make an amount of 0.
    if amount == 0:
        return 0

    # A negative amount means this recursive path does not work.
    if amount < 0:
        return -1

    minimum_coins = float("inf")

    # Try using each coin and solve the remaining amount.
    for coin in coins:
        result = coin_change_recursive(
            coins,
            amount - coin,
        )

        # Only use results that successfully made exact change.
        if result != -1:
            minimum_coins = min(
                minimum_coins,
                result + 1,
            )

    # No combination of coins could make the amount.
    if minimum_coins == float("inf"):
        return -1

    return minimum_coins


def coin_change_memoized(coins, amount, memo):
    """
    Find the minimum number of coins using top-down memoization.

    Parameters
    ----------
    coins : list[int]
        The available coin denominations.

    amount : int
        The target amount.

    memo : dict
        Stores answers to previously solved amounts.

    Returns
    -------
    int
        The minimum number of coins needed, or -1 if exact change
        cannot be made.
    """

    # No coins are needed to make an amount of 0.
    if amount == 0:
        return 0

    # A negative amount means this recursive path does not work.
    if amount < 0:
        return -1

    # Return the saved result if this amount was already solved.
    if amount in memo:
        return memo[amount]

    minimum_coins = float("inf")

    # Try each coin and recursively solve the remaining amount.
    for coin in coins:
        result = coin_change_memoized(
            coins,
            amount - coin,
            memo,
        )

        if result != -1:
            minimum_coins = min(
                minimum_coins,
                result + 1,
            )

    # Store the result before returning it.
    if minimum_coins == float("inf"):
        memo[amount] = -1
    else:
        memo[amount] = minimum_coins

    return memo[amount]


def coin_change_dp(coins, amount):
    """
    Find the minimum number of coins using bottom-up tabulation.

    Parameters
    ----------
    coins : list[int]
        The available coin denominations.

    amount : int
        The target amount.

    Returns
    -------
    int
        The minimum number of coins needed, or -1 if exact change
        cannot be made.
    """

    # Begin by treating every amount as impossible to make.
    dp = [float("inf")] * (amount + 1)

    # No coins are needed to make an amount of 0.
    dp[0] = 0

    # Build answers from the smallest amount to the target amount.
    for current_amount in range(1, amount + 1):
        for coin in coins:

            # The coin can only be used if it is not larger
            # than the current amount.
            if coin <= current_amount:
                dp[current_amount] = min(
                    dp[current_amount],
                    dp[current_amount - coin] + 1,
                )

    # The amount is impossible if its value was never updated.
    if dp[amount] == float("inf"):
        return -1

    return dp[amount]


def time_algorithm(function, coins, amount, trials=3):
    """
    Run an algorithm several times and return its average runtime.

    A new memo dictionary is created for each memoized trial so that
    every timing starts without previously saved answers.
    """

    runtimes = []

    for _ in range(trials):
        start_time = time.perf_counter()

        if function == coin_change_memoized:
            result = function(coins, amount, {})
        else:
            result = function(coins, amount)

        end_time = time.perf_counter()
        runtimes.append(end_time - start_time)

    average_runtime = sum(runtimes) / trials

    return result, average_runtime


def run_benchmark():
    """
    Compare the performance of the recursive, memoized, and bottom-up
    approaches across several target amounts.
    """

    coins = [1, 2, 5]

    # The amounts stay relatively small because the naive recursive
    # approach becomes slow much faster than the DP approaches.
    amounts = [5, 10, 15, 20, 25]

    recursive_times = []
    memoized_times = []
    dp_times = []

    print("Running empirical comparison...")
    print("Coins:", coins)
    print()
    print("Amount | Recursive | Memoized | Bottom-Up DP")

    for amount in amounts:
        recursive_result, recursive_time = time_algorithm(
            coin_change_recursive,
            coins,
            amount,
        )

        memoized_result, memoized_time = time_algorithm(
            coin_change_memoized,
            coins,
            amount,
        )

        dp_result, dp_time = time_algorithm(
            coin_change_dp,
            coins,
            amount,
        )

        # All three approaches should return the same answer.
        assert recursive_result == memoized_result == dp_result

        recursive_times.append(recursive_time)
        memoized_times.append(memoized_time)
        dp_times.append(dp_time)

        print(
            f"{amount:6} | "
            f"{recursive_time:.9f} | "
            f"{memoized_time:.9f} | "
            f"{dp_time:.9f}"
        )

    create_plot(
        amounts,
        recursive_times,
        memoized_times,
        dp_times,
    )

    print()
    print("All three approaches returned matching answers.")
    print("Performance plot saved as results.png.")


def create_plot(
    amounts,
    recursive_times,
    memoized_times,
    dp_times,
):
    """Create and save a performance comparison plot."""

    plt.figure(figsize=(9, 6))

    plt.plot(
        amounts,
        recursive_times,
        marker="o",
        label="Naive Recursive",
    )

    plt.plot(
        amounts,
        memoized_times,
        marker="o",
        label="Top-Down Memoized",
    )

    plt.plot(
        amounts,
        dp_times,
        marker="o",
        label="Bottom-Up DP",
    )

    # A logarithmic scale makes the very small DP times easier to see.
    plt.yscale("log")

    plt.xlabel("Target Amount")
    plt.ylabel("Average Runtime in Seconds (Log Scale)")
    plt.title("Coin Change Performance Comparison")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.savefig("results.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    # Confirm the required example before running the benchmark.
    example_coins = [1, 2, 5]
    example_amount = 11

    recursive_result = coin_change_recursive(
        example_coins,
        example_amount,
    )

    memoized_result = coin_change_memoized(
        example_coins,
        example_amount,
        {},
    )

    dp_result = coin_change_dp(
        example_coins,
        example_amount,
    )

    print("Required Example")
    print("Coins:", example_coins)
    print("Amount:", example_amount)
    print("Recursive minimum coins:", recursive_result)
    print("Memoized minimum coins:", memoized_result)
    print("Bottom-up DP minimum coins:", dp_result)
    print()

    run_benchmark()