   M S B A M L   `   `   `  ����K  GMultiDataTrigger, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null3clr-namespace:MultiDataTriggerMultiDataTrigger  5   	   !    MultiDataTrigger.MainWindow   5   	   W SPresentationCore, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   0localclr-namespace:MultiDataTrigger     5   	     � Title$  Multi Data Trigger��5   	   $	��150��6$   $	��350��61   .��5	      �� $��Center=�6   $��Center=�6.   .+�5
   
   �� -   5         ��Name$ 
chkLicense��5
      $%��Yes, I accept license agreement��6'   �� 5   
   -   5        $ chkTerms��5      $&�� Yes, I accept Terms & Conditions��6%   �� 5   
   $��Center=�6   $��0,20,0,0q�6.   $��20(�6@   $��Register��6N   ��5      �� 5       �� 
TargetType" ��6   .�5      ��  �� Property � {� �� Value$ False��62    �� Triggers 5      ^� 5       ^� 
Conditions 5      �� 5   "    �� Binding 6,   ��  �� ElementName$ 
chkLicense��	 �� Path$	 	IsChecked�
 �� Value
 True6g   �� 5   "    6,   �� $ chkTerms��$	 	IsChecked�
 True6e   .0�5      ��  � {�$
 True��6:   5      5      5      5      5      