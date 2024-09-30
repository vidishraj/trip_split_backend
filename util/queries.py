
class Queries:

    """ Travel Queries """

    fetchTripsQuery: str = f"select * from travelSchema.trips;"
    createTripQuery: str = f"INSERT INTO `travelSchema`.`trips` (`tripTitle`) VALUES (%s)"

    fetchUsers: str = "select * from travelSchema.users;"
    fetchUsersForSpecificTrip: str = "select * from travelSchema.users where tripId= %s;"
    createUser: str = "INSERT INTO `travelSchema`.`users` (`userName`, `tripId`) VALUES (%s, %s)"
    # delete user to be only used if no expenses attached
    deleteUser: str = "DELETE FROM `travelSchema`.`users` where userId = %s;"
    updateUserName: str = "Update `travelSchema`.`users` Set userName = %s where userId = %s;"

    insertExpense: str = "INSERT INTO `travelSchema`.`expenses` (`expenseDate`,`expenseDesc`," \
                         "`expenseAmount`,`expensePaidBy`,`expenseSplitBw`,`tripId`) VALUES" \
                         "(%s, %s, %s, %s, %s, %s)"
    fetchExpenses: str = "select * from `travelSchema`.`expenses`;"
    fetchExpensesFromTrip: str = "select * from `travelSchema`.`expenses` where tripId = %s;"
    fetchExpensesPaidByUserInTrip: str = "select * from `travelSchema`.`expenses` where expensePaidBy = %s and tripId " \
                                         "= %s; "
    # No updating expense. Just delete and reinsert new details.
    deleteExpense: str = "Delete from `travelSchema`.`expenses` where expenseId = %s;"
    # Update on individual attributes can be handles dynamically. Everything should be edittable.
    # Trigger complete update if amount, paidBy or splitBw is changed. Else build query.

    createBalance = "INSERT INTO `travelSchema`.`Balance` (`tripId`,`userId`,`expenseId`,`moneyPaid`," \
                    "`moneyBorrowed`,`currencyRate`, borrowedFrom) VALUES(%s, %s, %s, %s, %s, %s, %s);"
    fetchBalance: str = "Select * from `travelSchema`.`Balance`;"
    fetchBalanceFromTrip: str = "Select * from `travelSchema`.`Balance` where tripId = %s"
    fetchBalanceForUserFromTrip: str = "Select * from `travelSchema`.`Balance` where userId = %s and tripId = %s;"
    # Might be not necessary cause of cascade?
    deleteBalance = "delete from `travelSchema`.`Balance` where tripId = %s and expenseId = %s;"
