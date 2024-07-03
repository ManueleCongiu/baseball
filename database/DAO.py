from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT(YEAR) 
                   FROM teams t 
                   WHERE `year` >= 1985 
                   ORDER BY `year` DESC """

        cursor.execute(query)

        for row in cursor:
            result.append(row["YEAR"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYears(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                   FROM teams t 
                   WHERE `year` = %s """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeams(year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.teamCode, t.ID, SUM(s.salary) as totSalary
                    FROM salaries s, teams t, appearances a
                    WHERE s.`year` = t.`year` and t.`year` = a.`year` 
                    AND a.`year` = %s
                    AND t.ID = a.teamID 
                    AND s.playerID = a.playerID 
                    GROUP BY t.teamCode """

        cursor.execute(query, (year,))

        result = {}
        for row in cursor:
            #result.append((idMap[row["ID"]], row["totSalary"]))
            result[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return result
