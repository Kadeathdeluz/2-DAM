   M S B A M L   `   `   `  ����C  ?Academia, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null#clr-namespace:AcademiaAcademia  5          Academia.CreateCourse   5      R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5      R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5      Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5      @d2http://schemas.microsoft.com/expression/blend/2008     5      (localclr-namespace:Academia     5        N� Title$  Crear Curso��5      .��5
      � $��20q�6    � RowDefinitions 5   
   �� 5      $
��Auto �6   �� 5      $
��Auto �6   �� 5      $
��Auto �6   �� 5      $
��Auto �6   �� 5      $
��Auto �6   �� 5      $
��Auto �6   �� 5      $
��Auto �6   .+�5   
   �� $��Nombre del Curso:��6   $��14(�6-   $��0��6;   �� 5   
   -   5         ��Name$ courseNameTextBox��5      $��1��6-   $	��250��6:   $	��0,5q�6F   �� 5   
   $��
Duración:��6   $��14(�6%   $��2��63    � 
InputScope$ Number��6@   �� 5   
   -   5        $ durationTextBox��5      $��3��6+   $	��250��68   $	��0,5q�6D   �� 5   
   $��	Profesor:��6   $��14(�6%   $��4��63   �� 5   
   -   5        $ professorNameTextBox��5      $��5��60   $	��250��6=   $	��0,5q�6I   �� 5   
    �� Orientation$ 
Horizontal=�6   $��6��6.   $
��0,10q�6;   $��Center=�6I   .+�5      �� -   5        $��Aceptar��5      $	��100��6'   $��5q�63   6>   �� 5       -   5        $��Cancelar��5       $	��100��6(   $��5q�64   6?   5!      5"      5#      