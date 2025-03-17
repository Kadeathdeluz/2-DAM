package ADAbeans;

import java.sql.*;

/**
 * =====================================================================
 * Auxiliary class. DB Management
 * @author Abelardo Martínez. Based and modified from Sergio Badal
 * =====================================================================
 */

public class DBBean {

	/*
	 * ------------------------------------------
	 * CONSTANTS AND VARIABLES
	 * ------------------------------------------
	 */
	/*
	 * Database name, user and password
	 */
	private static final String DBNAME = "DBProducts";
	private static final String DBUSER = "mavenuser";
	private static final String DBPASSWORD = "ada0486";

	private static final String CONN_URL = "jdbc:mysql://localhost:3306/" + DBNAME
			+ "?useSSL=false&useTimezone=true&serverTimezone=UTC&allowPublicKeyRetrieval=true";
    private Connection cnDB = null;

    /*
	 * ------------------------
	 * SQL QUERIES
	 * ------------------------
	 */
	private static final String INSERT = " INSERT INTO orders (idp, amount)" + " VALUES (?, ?)";
	
    /*
	 * ------------------------------------------
	 * METHODS
	 * ------------------------------------------
	 */
	/*
	 * Empty constructor. Establish the connection to the DB
	 */
    public DBBean() {
        try {
            // This will load the MySQL driver, each DB has its own driver
            Class.forName("com.mysql.cj.jdbc.Driver");
            // Setup the connection with the DB
            cnDB = DriverManager.getConnection(CONN_URL,DBUSER,DBPASSWORD);
            System.out.println("Connected to the database.");
        } catch (ClassNotFoundException | SQLException sqle) {
            System.out.println("Got an exception (connecting)!");
            System.out.println(sqle.getMessage());
        }
    }

    /*
   	 * --------------------
   	 * CRUD OPERATIONS
   	 * --------------------
   	 */
    /*
     * Insert a new order into orders table
     */
    public static void insertOrder(ProductBean objProductBean, int iAmount) {
        System.out.println("Inserting...");
        try {
        	//create a new connection to the DB
            DBBean DB = new DBBean();
            
            // create the MySQL insert prepared statement
            PreparedStatement pstaSQLSelect = DB.cnDB.prepareStatement(INSERT);
            pstaSQLSelect.setInt(1, objProductBean.getiProductID());
            pstaSQLSelect.setInt(2, iAmount);

            // execute the prepared statement
            pstaSQLSelect.execute();

            //close DB connection
            DB.closeDBConnection();
            //show information about the new created order
            System.out.println("Order inserted (idp=" + objProductBean.getiProductID()
                    + " amount=" + iAmount + ")");
        } catch (SQLException sqle) {
            System.out.println("Got an exception (inserting)!");
            System.out.println(sqle.getMessage());
        }
    }

    /*
     * Close the connection to the DB
     */
    private void closeDBConnection() {
        try {
            if (cnDB != null) {
            	cnDB.close();
            }
        } catch (Exception exe) {
        	System.out.println("Exception while closing" + exe.getMessage());
        }
    }

}
