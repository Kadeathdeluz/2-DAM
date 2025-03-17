package ADAbeans;

import java.beans.*;
import java.io.Serializable;

/**
 * =====================================================================
 * Object ProductBean. SOURCE
 * @author Abelardo Martínez. Based and modified from Sergio Badal
 * =====================================================================
 */

public class ProductBean implements Serializable {
    
	/*
	 * ------------------------------------------
	 * ATTRIBUTES
	 * ------------------------------------------
	 */
	private static final long serialVersionUID = 1L;
    private int iProductID;
	private String stDescription;
    private float fPrice;
    private int iCurrentstock;
    private int iMinstock;

    private PropertyChangeSupport propertySupport;

    /*
	 * ------------------------------------------
	 * METHODS
	 * ------------------------------------------
	 */
	/*
	 * Empty constructor
	 */
    public ProductBean() {
        propertySupport = new PropertyChangeSupport(this);
    }

    /*
	 * Constructor with all fields
	 */
    public ProductBean(int iProductID, String stDescription, float fPrice, int iCurrentstock, int iMinstock) {
        propertySupport = new PropertyChangeSupport(this);
        this.iProductID = iProductID;
        this.stDescription = stDescription;
        this.fPrice = fPrice;
        this.iCurrentstock = iCurrentstock;
        this.iMinstock = iMinstock;
    }

    /*
	 * ------------------------------------------
	 * GETTERS
	 * ------------------------------------------
	 */
    public int getiProductID() {
        return iProductID;
    }
    
    public String getstDescription() {
        return stDescription;
    }

    public float getfPrice() {
        return fPrice;
    }

    public int getiCurrentStock() {
        return iCurrentstock;
    }

    public int getiMinStock() {
        return iMinstock;
    }
    
    /*
	 * ------------------------------------------
	 * SETTERS
	 * ------------------------------------------
	 */
    public void setiProductID(int iProductID) {
        this.iProductID = iProductID;
    }
    
    public void setstDescription(String stDescription) {
        this.stDescription = stDescription;
    }

    public void setPrice(float fPrice) {
        this.fPrice = fPrice;        
    }
    
    public void setiCurrentStock(int iNewCurrentStock) {

        int iOldCurrentStock = this.iCurrentstock;
        this.iCurrentstock = iNewCurrentStock;
        // If NEW current stock is below minimum, order this product!
        if (this.iCurrentstock < getiMinStock())
        {
        	//Call OrderBean
            propertySupport.firePropertyChange("currentStockBelowMinStock", iOldCurrentStock, this.iCurrentstock);
        }
    }
    
    public void setiMinStock(int iNewMinStock) {
        
        int iOldMinstock = this.iMinstock;
        this.iMinstock = iNewMinStock;
        // If MIN stock has been raised over current stock, order this product!
        if (this.iMinstock > getiCurrentStock()) 
        {
        	//Call OrderBean
            propertySupport.firePropertyChange("minStockRaisedOverCurrentStock", iOldMinstock, this.iMinstock);
        }
    }

    /*
	 * ---------------------------
	 * LISTENERS. PROPERTYCHANGE
	 * ---------------------------
	 */
    public void addPropertyChangeListener(PropertyChangeListener listener) {
        propertySupport.addPropertyChangeListener(listener);
    }

    public void removePropertyChangeListener(PropertyChangeListener listener) {
        propertySupport.removePropertyChangeListener(listener);
    }

}
