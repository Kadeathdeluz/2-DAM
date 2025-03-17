package ADAbeans;

import java.beans.*;
import java.io.Serializable;

/**
 * =====================================================================
 * Object OrderBean. LISTENER
 * @author Abelardo Martínez. Based and modified from Sergio Badal
 * =====================================================================
 */

public class OrderBean implements Serializable, PropertyChangeListener {

	/*
	 * ------------------------------------------
	 * ATTRIBUTES
	 * ------------------------------------------
	 */
	private static final long serialVersionUID = 1L;
	private int iOrdernumber;
    private ProductBean objProductBean;
    private int iAmount;

    /*
	 * ------------------------------------------
	 * METHODS
	 * ------------------------------------------
	 */
	/*
	 * Empty constructor
	 */
    public OrderBean() {

    }

    /*
	 * Constructor with all fields
	 */
    public OrderBean(int iOrdernumber, int iAmount, ProductBean objProductBean) {
        this.iOrdernumber = iOrdernumber;
        this.objProductBean = objProductBean;
        this.iAmount = iAmount;
    }

    /*
	 * ------------------------------------------
	 * GETTERS
	 * ------------------------------------------
	 */
    public int getiOrderNumber() {
        return iOrdernumber;
    }

    public int getiAmount() {
        return iAmount;
    }

    public ProductBean getobjProductBean() {
        return this.objProductBean;
    }

    /*
	 * ------------------------------------------
	 * SETTERS
	 * ------------------------------------------
	 */
    public void setiOrderNumber(int iOrdernumber) {
        this.iOrdernumber = iOrdernumber;
    }
    
    public void setiAmount(int iAmount) {
        this.iAmount = iAmount;
    }

    public void setobjProductBean(ProductBean objProductBean) {
        this.objProductBean = objProductBean;
    }
    
    /*
   	 * -------------------------
   	 * LISTENERS. EVENTS RAISED
   	 * -------------------------
   	 */
    public void propertyChange(PropertyChangeEvent pceEvent) {
    	int iAmountOrder = objProductBean.getiMinStock() - objProductBean.getiCurrentStock();
    	
        if (pceEvent.getPropertyName().equals("currentStockBelowMinStock"))
        {
        	// Current stock is below minimum
            System.out.printf("[OrderBean says... ]%n");
            System.out.printf("Current stock is now less than minimum stock!%n");
            System.out.printf("=> Old current Stock: %d%n", pceEvent.getOldValue());
            System.out.printf("=> New current Stock: %d%n", pceEvent.getNewValue());
            System.out.printf("It will place an order for this product: %s%n",
            	objProductBean.getstDescription());
            //create a new order in the DB. Amount = minStock - Current stock
            DBBean.insertOrder(objProductBean, iAmountOrder);
        }
        
        if (pceEvent.getPropertyName().equals("minStockRaisedOverCurrentStock"))
        {
        	// MIN stock has been raised over current stock
            System.out.printf("[OrderBean says... ]%n");
            System.out.printf("Minimum stock is now greater than current stock!%n");
            System.out.printf("Old minstock Stock: %d%n", pceEvent.getOldValue());
            System.out.printf("New minstock Stock: %d%n", pceEvent.getNewValue());
            System.out.printf("It will place an order for this product: %s%n",
            	objProductBean.getstDescription());
            //create a new order in the DB. Amount = minStock - Current stock
            DBBean.insertOrder(objProductBean, iAmountOrder);
        }
    }

}
