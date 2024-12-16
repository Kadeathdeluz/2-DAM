using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace controlesC
{
    /// <summary>
    /// Lógica de interacción para MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        /** --------------- VARIABLES --------------- */
        private Button[,] botones;

        public MainWindow()
        {
            InitializeComponent();

            // Crea los botones
            CrearBotones();
        }

        private void CrearBotones() {
            // Primero limpiamos la parrilla
            ugridTablero.Children.Clear();
            
            botones = new Button[3,6];

            int numBoton = 1;

            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 6; j++) {
                    Button boton = new Button();
                    
                    String textoBoton = "";
                    // Si el número del botón es par, le asignamos el nombre, si no, asignamos el del siguiente, que será par
                    if (numBoton % 2 == 0)
                    {
                        textoBoton = "Botón " + numBoton.ToString();
                    }
                    else {
                        textoBoton = "Botón " + (numBoton+1).ToString();
                    }
                    // Le damos nombre
                    boton.Name = $"btn_{i}_{j}";
                    // Cambiamos el contenido del botón a "Botón {número par}"
                    boton.Content = textoBoton;
                    // Añadimos el evento de click derecho
                    boton.MouseRightButtonDown += Boton_ClickDerecho;
                    // Adicionalmente añadimos un evento para resetear la casilla y probar varias veces el evento de click derecho
                    boton.Click += Boton_Click;

                    // Ubicamos el botón en el "tablero"
                    Grid.SetRow(boton, i);
                    Grid.SetColumn(boton, j);
                    // Centramos el botón en horizontal y vertical
                    //boton.HorizontalAlignment = HorizontalAlignment.Center;
                    //boton.VerticalAlignment = VerticalAlignment.Center;
                    // Lo añadimos
                    ugridTablero.Children.Add(boton);

                    botones[i,j] = boton;

                    numBoton++;
                }
            }

        }


        private void Boton_ClickDerecho(object sender, MouseButtonEventArgs e)
        {
            // El botón que ha sido clickado
            Button botonActual = (Button)sender;
            // Cambiamos el fondo a BlueViolet
            botonActual.Background = Brushes.BlueViolet;
            
        }

        /** Cambia el color de la casilla a Naranja (NOTA: es un extra) */
        private void Boton_Click(object sender, RoutedEventArgs e)
        {
            // El botón que ha sido clickado
            Button botonActual = (Button)sender;
            // Cambiamos el fondo a BlueViolet
            botonActual.Background = Brushes.Orange;
        }
    }
}
