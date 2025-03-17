package TestADAbeans;

import ADAbeans.*;


/**
 * =====================================================================
 * Main programme to interact among JavaBeans
 * @author Abelardo Martínez. Based and modified from Sergio Badal
 * =====================================================================
 */

public class TestADAbeans {
    
	public static void main(String[] stArgs) {
		/*
		 * Creating the objects
		 */
		//Object source
        //ProductBean(int iProductid, String stDescription, float fPrice, int iCurrentstock, int iMinstock)
        //Setting currentStock to 101 units and minimumStock to 100 units
        ProductBean objProductBean = new ProductBean(1, "Robot hoover", 399, 101, 100);
        //Object listener
        OrderBean objOrderBean = new OrderBean();
        /*
         * Assign the object source to the listener
         * Start the listener object
         */
        objOrderBean.setobjProductBean(objProductBean);
        objProductBean.addPropertyChangeListener(objOrderBean);
        /*
         * Firing events 
         */
        //Setting currentStock to 40 (below the minimum advisable)
        System.out.println("****** product.setCurrentStock(40):");
        objProductBean.setiCurrentStock(40);
        //Setting minimumStock to 50 (over the current stock)
        System.out.println("****** product.setMinStock(50):");
        objProductBean.setiMinStock(50);
    }
}
