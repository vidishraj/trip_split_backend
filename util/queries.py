class Queries:
    """ Travel Queries """

    fetchTripsQuery: str = """SELECT t.tripIdShared, t.tripTitle, t.currencies 
    FROM `travelSchema_v2`.`trips` AS t 
    JOIN `travelSchema_v2`.`userTrips` AS u ON t.tripIdShared = u.tripId 
    WHERE u.userId = :email;"""

    createTripQuery: str = """INSERT INTO `travelSchema_v2`.`trips` 
    (`tripTitle`, `currencies`, `tripIdShared`) 
    VALUES (:tripTitle, :currencies, :tripIdShared);"""

    insertTripForAdminUser: str = """INSERT INTO `travelSchema_v2`.`users` 
    (`userName`, `tripId`) 
    VALUES (:userName, :tripId);"""

    checkIfUserHasAuth: str = """SELECT COUNT(1) 
    FROM `travelSchema_v2`.`userTrips` 
    WHERE `userId` = :userId AND `tripId` = :tripId;"""

    checkIfRequestsExists: str = """SELECT COUNT(1) 
    FROM `travelSchema_v2`.`tripRequest` 
    WHERE `userId` = :userId AND `tripId` = :tripId;"""

    checkIfIdExists: str = """SELECT COUNT(1) 
    FROM `travelSchema_v2`.`trips` 
    WHERE `tripIdShared` = :tripIdShared;"""

    fetchIdForEmail: str = """SELECT userId 
    FROM `travelSchema_v2`.`users` 
    WHERE `email` = :email;"""

    connectUserToTrip: str = """INSERT INTO `travelSchema_v2`.`userTrips`
    (`userId`, `tripId`) 
    VALUES (:userId, :tripId);"""

    registerUserRequest: str = """INSERT INTO `travelSchema_v2`.`tripRequest`
    (`userId`, `tripId`) 
    VALUES (:userId, :tripId);"""

    deleteRequest: str = """DELETE FROM `travelSchema_v2`.`tripRequest` 
    WHERE `userId` = :userId AND `tripId` = :tripId;"""

    fetchUsers: str = "SELECT * FROM `travelSchema_v2`.`users`;"

    fetchTripRequestForTrip: str = """SELECT u.userId, u.userName, u.email 
    FROM `travelSchema_v2`.`tripRequest` AS t 
    JOIN `travelSchema_v2`.`users` AS u ON t.userId = u.userId 
    WHERE t.tripId = :tripId;"""

    fetchUsersForSpecificTrip: str = """SELECT ut.userId, ut.userName, u.tripId, ut.email 
    FROM `travelSchema_v2`.`userTrips` AS u 
    JOIN `travelSchema_v2`.`users` AS ut ON ut.userId = u.userId 
    WHERE u.tripId = :tripId;"""

    createUser: str = """INSERT INTO `travelSchema_v2`.`users`
    (`userName`, `email`) 
    VALUES (:userName, :email);"""

    deleteUser: str = """DELETE FROM `travelSchema_v2`.`users` 
    WHERE `userId` = :userId;"""

    checkIfUserHasExpenses: str = """SELECT COUNT(*) 
    FROM `travelSchema_v2`.`expenses` 
    WHERE JSON_CONTAINS(`expenseSplitBw`, :userId, '$') OR `expensePaidBy` = :userId;"""

    updateUserName: str = """UPDATE `travelSchema_v2`.`users` 
    SET `userName` = :userName 
    WHERE `userId` = :userId;"""

    insertExpense: str = """INSERT INTO `travelSchema_v2`.`expenses` 
    (`expenseDate`, `expenseDesc`, `expenseAmount`, `expensePaidBy`, `expenseSplitBw`, `tripId`) 
    VALUES (:expenseDate, :expenseDesc, :expenseAmount, :expensePaidBy, :expenseSplitBw, :tripId);"""

    fetchExpenses: str = "SELECT * FROM `travelSchema_v2`.`expenses`;"

    fetchExpensesFromTrip: str = """SELECT * 
    FROM `travelSchema_v2`.`expenses` 
    WHERE `tripId` = :tripId;"""

    fetchExpensesFromTripJoined: str = """SELECT e.expenseId, e.expenseDate, e.expenseDesc, e.expenseAmount, 
    e.expensePaidBy, e.expenseSplitBw, b.tripId, b.userId, b.amount, b.borrowedFrom 
    FROM `travelSchema_v2`.`expenses` AS e 
    JOIN `travelSchema_v2`.`Balance` AS b ON e.expenseId = b.expenseId 
    WHERE e.tripId = :tripId;"""

    fetchExpensesPaidByUserInTrip: str = """SELECT * 
    FROM `travelSchema_v2`.`expenses` 
    WHERE `expensePaidBy` = :userId AND `tripId` = :tripId;"""

    deleteExpense: str = """DELETE FROM `travelSchema_v2`.`expenses` 
    WHERE `expenseId` = :expenseId;"""

    updateExpense: str = """UPDATE `travelSchema_v2`.`expenses` 
    SET `expenseDate` = :expenseDate, `expenseDesc` = :expenseDesc, 
    `expenseAmount` = :expenseAmount, `expensePaidBy` = :expensePaidBy, 
    `expenseSplitBw` = :expenseSplitBw 
    WHERE `expenseId` = :expenseId;"""

    createBalance: str = """INSERT INTO `travelSchema_v2`.`Balance` 
    (`tripId`, `userId`, `expenseId`, `amount`, `borrowedFrom`) 
    VALUES (:tripId, :userId, :expenseId, :amount, :borrowedFrom);"""

    fetchBalance: str = "SELECT * FROM `travelSchema_v2`.`Balance`;"

    fetchBalanceFromTrip: str = """SELECT * 
    FROM `travelSchema_v2`.`Balance` 
    WHERE `tripId` = :tripId;"""

    fetchBalanceForUserFromTrip: str = """SELECT * 
    FROM `travelSchema_v2`.`Balance` 
    WHERE `userId` = :userId AND `tripId` = :tripId;"""

    deleteBalance: str = """DELETE FROM `travelSchema_v2`.`Balance` 
    WHERE `tripId` = :tripId AND `expenseId` = :expenseId;"""
