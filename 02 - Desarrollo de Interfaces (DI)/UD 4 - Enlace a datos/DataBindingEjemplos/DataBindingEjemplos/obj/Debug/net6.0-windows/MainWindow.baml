   M S B A M L   `   `   `  ����N  JDataBindingEjemplos, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null9!clr-namespace:DataBindingEjemplosDataBindingEjemplos  5   	   $    DataBindingEjemplos.MainWindow   5   	   W SPresentationCore, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   3local!clr-namespace:DataBindingEjemplos     5   	     � Title$  
MainWindow��5   	   $	��450��6   $	��800��6)   .��5	      �  � RowDefinitions 5
   
   �� 5      $��* �6   �� 5      $��* �6   �� 5      $��* �6    � ColumnDefinitions 5   
   �� 5      $��* �6   �� 5      $��* �6   �� 5      $��* �6   .+�5   
   �� $��0��6   $��0��6!   $��Center=�5      $��Center=�5      �� 5   
   $�Hola, ��6   $
��Bold"�6   
����  �6.    �� 5   
   $-�'esto es un ejemplo de texto formateado.��6   $��Italic$�6=   
���  ��6P   5      �� 5   
   $��0��6   $��0��6!   $��3��61   $��10q�5      $��Center=�5      $��Center=�5       ��5      �� *Value+ �� ElementName$ fontSizeSlider���� 5!      $�
Font Size:��6    �� 5"      �6   �� *Value+$ fontSizeSlider�� �� Mode$ OneWay=�5#      �� 5%   
   -   5         ��Name$ fontSizeSlider��5&      $��0��5%      $��1��6    � Minimum$ 10Q�5'       � Maximum$ 40Q�6    � Value$ 15Q�6+   $��10q�5(      $��Bottom=�5)      �� 5+   
   $��1��6   $��0��6   $��3��6/   $��10q�5.      $��Center=�5/      $��Center=�50      ��5,      �� $ miSlider��	 �� Path$	 Value�$ TwoWay=���5-      �� *Value+$ miSlider��.��50   -   51      �� 53   
   -   5        $ miSlider��54      $��1��53      $��1��6   $ 10Q�55      $ 40Q�6   $ 15Q�6+   $��10q�56      $��Bottom=�57      58      59      