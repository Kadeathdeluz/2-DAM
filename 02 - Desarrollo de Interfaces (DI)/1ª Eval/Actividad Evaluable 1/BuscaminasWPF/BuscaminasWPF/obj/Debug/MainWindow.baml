   M S B A M L   `   `   `  ����H  DBuscaminasWPF, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null-clr-namespace:BuscaminasWPFBuscaminasWPF  5   	       BuscaminasWPF.MainWindow   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   -localclr-namespace:BuscaminasWPF     5   	     � Title$  
Buscaminas��5   	   $	��450��5	   	   $	��450��6    � 
ResizeMode$ NoResize=�5
   	    � 	Resources 5         DigitalFont��%M   &	        *�5   
   /+pack://application:,,,/Resources/#Digital-7)�6V   5      .��5      �  � RowDefinitions 5   
   �� 5      $��60 �6   �� 5      $��* �6   .+�5   
   �� -   5         ��Name$ lblCronometro��5      $	��000��6'   $��0,0,24,0q�5      $��Right=�5      $��Center=�5      #��[  5      $��36(�5      
���  ��5      �� 5   
   -   5        $ lblMinas��5      $	��010��6"   $��24,0,0,0q�5      $
��Left=�5      $��Center=�5      #��[  5       $��36(�5!      
���  ��5"      �� 5$   
   -   5         ��Name$ botonReinicio��5$      $��0��6   $��40��5%      $��40��6   $��Center=�5&      $��Center=�5'      .��5)      �� -   5         ��Name$ iconoReinicio��5)      $��Resources/smile.png��5*      $
��Fill=�5+      5,      A� 5.   
   -   5         A�Name$ gameGrid��5/      $��1��5.      $��20q�50      52      53      54      