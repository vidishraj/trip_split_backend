class Queries:
    """ Travel Queries """

    fetchTripsQuery: str = f""" SELECT t.tripIdShared, t.tripTitle, t.currencies FROM `travelSchema_v2`.`trips` as t 
    JOIN `travelSchema_v2`.`userTrips` as u ON t.tripIdShared = u.tripId WHERE u.userId = %s; """
    createTripQuery: str = f"INSERT INTO `travelSchema_v2`.`trips` (`tripTitle`, `currencies`, `tripIdShared`) VALUES " \
                           f"(%s, %s, %s)"
    insertTripForAdminUser: str = "INSERT INTO `travelSchema_v2`.`users` (`userName`, `tripId`) VALUES (%s, %s)"
    checkIfUserHasAuth: str = "SELECT COUNT(1) FROM `travelSchema_v2`.`userTrips` WHERE `userId` = %s and " \
                              "tripId = %s;"
    checkIfRequestsExists: str = "SELECT COUNT(1) FROM `travelSchema_v2`.`tripRequest` WHERE `userId` = %s and " \
                                 "tripId = %s;"
    checkIfIdExists: str = "SELECT COUNT(1) FROM `travelSchema_v2`.`trips` WHERE `tripIdShared` = %s;"
    fetchIdForEmail: str = "SELECT userId FROM `travelSchema_v2`.`users` WHERE `email` = %s;"
    connectUserToTrip: str = "INSERT INTO `travelSchema_v2`.`userTrips`(`userId`,`tripId`)VALUES (%s, %s);"
    registerUserRequest: str = "INSERT INTO `travelSchema_v2`.`tripRequest`(`userId`,`tripId`)VALUES (%s, %s);"
    deleteRequest: str = "DELETE FROM `travelSchema_v2`.`tripRequest` where userId = %s and tripId = %s;"
    fetchUsers: str = "select * from travelSchema_v2.users;"

    fetchTripRequestForTrip: str = " Select u.userId, u.userName, u.email from `travelSchema_v2`.`tripRequest` as t " \
                                   "join `travelSchema_v2`.`users` as u on t.userId = u.userId and t.tripId = %s;"
    fetchUsersForSpecificTrip: str = "select ut.userId, ut.userName, u.tripId, ut.email  from " \
                                     "travelSchema_v2.userTrips " \
                                     "as u join travelSchema_v2.users as ut " \
                                     "on ut.userId= u.userId where tripId= %s;"
    createUser: str = "INSERT INTO `travelSchema_v2`.`users`(`userName`,`email`) VALUES ( %s, %s)"
    # delete user to be only used if no expenses attached
    deleteUser: str = "DELETE FROM `travelSchema_v2`.`users` where userId = %s;"
    checkIfUserHasExpenses: str = "SELECT count(*) FROM travelSchema_v2.expenses WHERE JSON_CONTAINS( expenseSplitBw, " \
                                  "%s,'$') or expensePaidBy=%s; "
    updateUserName: str = "Update `travelSchema_v2`.`users` Set userName = %s where userId = %s;"

    insertExpense: str = "INSERT INTO `travelSchema_v2`.`expenses` (`expenseDate`,`expenseDesc`," \
                         "`expenseAmount`,`expensePaidBy`,`expenseSplitBw`,`tripId`) VALUES" \
                         "(%s, %s, %s, %s, %s, %s)"
    fetchExpenses: str = "select * from `travelSchema_v2`.`expenses`;"
    fetchExpensesFromTrip: str = "select * from `travelSchema_v2`.`expenses` where tripId = %s;"
    fetchExpensesFromTripJoined: str = "select e.expenseId, e.expenseDate, e.expenseDesc, e.expenseAmount, " \
                                       "e.expensePaidBy, e.expenseSplitBw, b.tripId, b.userId, b.amount, " \
                                       "b.borrowedFrom from `travelSchema_v2`.`expenses` as e join " \
                                       "`travelSchema_v2`.`Balance` as b  on  e.expenseId=b.expenseId where e.tripId = " \
                                       "%s; "
    fetchExpensesPaidByUserInTrip: str = "select * from `travelSchema_v2`.`expenses` where expensePaidBy = %s and " \
                                         "tripId " \
                                         "= %s; "
    # No updating expense. Just delete and reinsert new details.
    deleteExpense: str = "Delete from `travelSchema_v2`.`expenses` where expenseId = %s;"

    updateExpense: str = "UPDATE `travelSchema_v2`.`expenses` SET `expenseDate` = %s,`expenseDesc` = %s," \
                         "`expenseAmount` = %s,`expensePaidBy` = %s,`expenseSplitBw` = %s WHERE " \
                         "`expenseId` = %s;"

    # Update on individual attributes can be handles dynamically. Everything should be edittable.
    # Trigger complete update if amount, paidBy or splitBw is changed. Else build query.

    createBalance = "INSERT INTO `travelSchema_v2`.`Balance` (`tripId`,`userId`,`expenseId`,`amount`," \
                    " borrowedFrom) VALUES(%s, %s, %s, %s, %s);"
    fetchBalance: str = "Select * from `travelSchema_v2`.`Balance`;"
    fetchBalanceFromTrip: str = "Select * from `travelSchema_v2`.`Balance` where tripId = %s"
    fetchBalanceForUserFromTrip: str = "Select * from `travelSchema_v2`.`Balance` where userId = %s and tripId = %s;"
    # Might be not necessary cause of cascade?
    deleteBalance = "delete from `travelSchema_v2`.`Balance` where tripId = %s and expenseId = %s;"
