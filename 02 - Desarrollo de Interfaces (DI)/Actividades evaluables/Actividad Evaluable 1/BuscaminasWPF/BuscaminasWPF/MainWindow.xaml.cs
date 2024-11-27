using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;

namespace BuscaminasWPF
{
    /// <summary>
    /// Lógica de interacción para MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        /** ---------------------- COSTANTES ---------------------- */
        // Atributos tablero
        private const int Filas = 9;
        private const int Columnas = 9;
        private const int NumMinas = 10;
        // Emojis (String)
        private const String EmojiMina = "💣";
        private const String EmojiBandera = "🚩";

        /** ---------------------- VARIABLES ---------------------- */
        private int minasRestantes; // Minas restantes (para el contador)
        private DispatcherTimer cronometro; // DispatcherTimer para actualizar el cronómetro "ingame"
        private int numClicks; // Contador con el número de clicks realizados (sólo cuenta clicks izquierdos)
        private Button btnReinicio; // Botón de reinicio
        private Button[,] botones; // Matriz con los botones del tablero (para deshabilitarlos al final)
        private bool[,] minas; // Matriz con las minas
        private bool gameOver = false; // Booleano que controla si hemos terminado el juego o no
        private int casillasReveladas; // Contador de casillas reveladas (para saber si hemos ganado o no)
        private int tiempo; // Contador para actualizar el cronómetro

        public MainWindow()
        {
            InitializeComponent();

            // Iniciamos toda la lógica y atributos
            Inicio();
        }
        /** ---------------------- MÉTODOS AUXILIARES ---------------------- */

        /* Establece los valores iniciales de todos los atributos e inicia el cronómetro */
        private void Inicio()
        {
            // Inicialmente el icono es Smile
            CambiarIconoReinicio("smile.png");
            // Creamos el tablero
            CrearTablero();
            // Insertamos las minas
            GenerarMinas();
            // Minas iniciales
            minasRestantes = NumMinas;
            ActualizarMinasRestantes();
            // El juego no ha terminado
            gameOver = false;
            // El temporizador a 0
            lblCronometro.Content = "000";
            tiempo = 0;
            // Ninguna casilla revelada
            casillasReveladas = 0;
            // Número de clicks a 0
            numClicks = 0;

            // Creamos el Timer y asociamos un intervalo en el que llamará a un método
            // Opcionalmente se puede iniciar el Timer al hacer el primer click, pero prefiero esta opción
            cronometro = new DispatcherTimer(); 
            cronometro.Interval = TimeSpan.FromSeconds(1); // Actualización cada 1 segundo
            cronometro.Tick += Actualizar_Cronometro; // Método al que llamará tras cada intervalo
            // Inicia el Timer (importante, si no no funciona)
            cronometro.Start();
        }

        /* Cambia el icono al botón de reinicio */
        private void CambiarIconoReinicio(String nombreImagen)
        {
            // Actualiza el icono a la imagen indicada
            iconoReinicio.Source = new BitmapImage(new Uri($"Resources/{nombreImagen}", UriKind.Relative)); // Cambiamos el icono mediante una Uri relativa
        }

        /* Crea el tablero de juego (matriz de botones) */
        private void CrearTablero()
        {
            // Primero limpiamos el tablero por si acaso
            gameGrid.Children.Clear();

            btnReinicio = botonReinicio;
            // Creamos la matriz que alojará los botones (Filas x Columnas)
            botones = new Button[Filas, Columnas];

            // Creamos los botones y los añadimos al tablero (gameGrid) y a la matriz
            for (int i = 0; i < Filas; i++)
            {
                for (int j = 0; j < Columnas; j++)
                {
                    // Creamos cada botón
                    Button boton = new Button();
                    boton.Name = $"btn_{i}_{j}"; // Le damos nombre
                    boton.Content = ""; // Ponemos el contenido a "vacío"

                    // Asignamos eventos a click izquierdo y derecho
                    boton.Click += Casilla_ClickIzquierdo;
                    boton.MouseRightButtonDown += Casilla_ClickDerecho;
                    // Establecemos la posición de los botones
                    Grid.SetRow(boton, i);
                    Grid.SetColumn(boton, j);
                    // Agregamos los botones al tablero (uniformGrid)
                    gameGrid.Children.Add(boton);
                    // Añadimos los botones a la matriz
                    botones[i, j] = boton;
                }
            }
        }

        /* Genera la matriz con las minas (inserta las minas de manera aleatoria en el tablero) */
        private void GenerarMinas()
        {
            // Creamos la matriz de minas
            minas = new bool[Filas, Columnas];
            Random random = new Random(); // Objeto de la clase Random (para elegir posiciones aleatorias)
            int minasColocadas = 0; // Inicialmente no hay minas colocadas

            //Mientras no estén todas las minas colocadas, intentará colocarlas
            while (minasColocadas < NumMinas)
            {
                //Elige al azar una fila (y para esa fila, una columna)
                int fila = random.Next(Filas);
                int columna = random.Next(Columnas);

                //Si en esa posición NO hay una mina, la inserta (asegura que haya NumMinas en juego)
                if (!minas[fila, columna])
                {
                    // La posición pasa a contener "true" (una mina)
                    minas[fila, columna] = true;
                    minasColocadas++;
                }
            }
        }

        /* Cuenta las minas en las casillas vecinas y retorna el número */
        private int ContarMinasAdyacentes(int fila, int columna)
        {
            int minasVecinas = 0;

            // Recorremos las 8 casillas adyacentes
            for (int i = -1; i <= 1; i++)
            {
                for (int j = -1; j <= 1; j++)
                {
                    int nuevaFila = fila + i;
                    int nuevaColumna = columna + j;

                    // Verificar que la nueva casilla esté dentro de los límites 
                    if (nuevaFila >= 0 && nuevaFila < Filas && nuevaColumna >= 0 && nuevaColumna < Columnas)
                    {
                        // Si hay una mina en la casilla vecina, incrementamos el contador
                        if (minas[nuevaFila, nuevaColumna])
                        {
                            minasVecinas++;
                        }
                    }
                }
            }
            // Finalmente retornamos el número de minas vecinas
            return minasVecinas;
        }

        /* Revelamos las casillas adyacentes de manera recursiva */
        private void RevelarCasillasAdyacentes(int fila, int columna)
        {
            // Recorremos las 8 casillas adyacentes (también se recorre la actual) 
            // De izquierda a derecha
            for (int i = -1; i <= 1; i++)
            {
                // De arriba abajo
                for (int j = -1; j <= 1; j++)
                {
                    int nuevaFila = fila + i;
                    int nuevaColumna = columna + j;
                    
                    // Verificar que la nueva casilla esté dentro de los límites, p.e. (-1, -1) está fuera, y (Filas,Columnas) también está fuera
                    if (nuevaFila >= 0 && nuevaFila < Filas && nuevaColumna >= 0 && nuevaColumna < Columnas)
                    {
                        Button boton = botones[nuevaFila, nuevaColumna];

                        // Solo revelar casillas que no hayan sido reveladas
                        if (boton.IsEnabled)
                        {
                            // Si el botón contiene una bandera, la "recogemos"
                            if ((String)boton.Content == EmojiBandera) {
                                boton.Content = "";
                                if (minasRestantes < NumMinas)
                                {
                                    minasRestantes++;
                                    ActualizarMinasRestantes();
                                }
                            }
                            // Deshabilitamos el botón para evitar volver a contarlo o que se pueda interactuar con él
                            boton.IsEnabled = false;

                            // Contar el número de minas adyacentes
                            int minasVecinas = ContarMinasAdyacentes(nuevaFila, nuevaColumna);

                            // Si la casilla no tiene minas cercanas, la revelamos y seguimos con las adyacentes de manera recursiva
                            if (minasVecinas == 0)
                            {
                                boton.Content = "";
                                RevelarCasillasAdyacentes(nuevaFila, nuevaColumna);
                            }
                            else
                            {
                                // Si tiene minas cercanas, mostramos el número de minas
                                boton.Content = minasVecinas.ToString();
                                // Decoramos el número con un color
                                boton.Foreground = ObtenerColorDeNumero(minasVecinas);
                            }

                            casillasReveladas++;
                        }
                    }
                }
            }
        }

        /* Obtiene el color según el número (devuelve*/
        private Brush ObtenerColorDeNumero(int numero)
        {
            // Dependiendo del número, será de un color (foreground)
            switch (numero)
            {
                case 1:
                    return Brushes.Blue; // Azul para 1
                case 2:
                    return Brushes.Green; // Verde para 2
                case 3:
                    return Brushes.Red; // Rojo para 3

                default:
                    return Brushes.Black;
            }
        }

        /* Termina el juego y libera los botones */
        private void TerminarJuego(bool win)
        {

            // Primero que nada, detenemos el cronómetro
            cronometro.Stop();

            // Creamos el mensaje que se mostrará al terminar el juego
            String mensajeFinal = "";

            gameOver = true;

            // Desactivamos todos los botones (de la matriz de botones)
            foreach (Button boton in botones)
            {
                // No queremos que la última mina se deshabilite (esto hace que no se muestre el borde rojo)
                // El botón que contiene la mina es la que hemos pulsado
                if ((String)boton.Content == EmojiMina)
                {
                    boton.IsEnabled = true;
                }
                else
                {
                    boton.IsEnabled = false;
                }
            }
            // Revelamos la posición de las minas
            RevelarMinas();
            // Actualizamos el contador de minas restantes
            minasRestantes = 0;
            ActualizarMinasRestantes();
            // En caso de ganar, imprime el mensaje ganador
            if (win)
            {
                // Cambiamos el contenido del botón (cambiamos la imagen)
                CambiarIconoReinicio("win.png");
                mensajeFinal += "\n¡HAS GANADO!";
            }
            // En caso de perder, imprime el mensaje perdedor
            else
            {
                // Cambiamos el contenido del botón (cambiamos la imagen)
                CambiarIconoReinicio("dead.png");
                mensajeFinal += "\n¡HAS PERDIDO!";
            }
            // Añadimos las estadísticas de la partida
            mensajeFinal += "\nESTADÍSTICAS: \n" +
                // Se añade el tiempo empleado
                $"Tiempo empleado: {tiempo} segundos" +
                // Finalmente se añaden los clicks realizados
                $"\nSe han realizado: {numClicks} clicks";



            MessageBox.Show(mensajeFinal);
        }

        /* Revela todas las minas */
        private void RevelarMinas()
        {
            // Recorremos toda la matriz de minas para mostrarla sobre el tablero
            for (int fila = 0; fila < Filas; fila++)
            {
                for (int columna = 0; columna < Columnas; columna++)
                {
                    if (minas[fila, columna]) // Si hay una mina en esta posición
                    {
                        // Encontrar el botón correspondiente en el tablero (en gameGrid se guarda como un array de Childs, no como una matriz)
                        Button casilla = (Button)gameGrid.Children[fila * Columnas + columna];

                        // Cambiar la apariencia del botón para mostrar la mina
                        casilla.Content = EmojiMina;
                    }
                }
            }
        }

        /* Actualiza las minas restantes en el contador */
        private void ActualizarMinasRestantes()
        {
            // Igual que para el tiempo "D3" formatea para obtener 3 dígitos (formato 000)
            lblMinas.Content = $"{minasRestantes:D3}";
        }

        /** ---------------------- EVENTOS ---------------------- */

        /* Acción que se realiza al hacer click en el botón de reinicio */
        private void BotonReinicio_Click(object sender, RoutedEventArgs e)
        {
            // Paramos el cronómetro antes que nada 
            if (cronometro.IsEnabled)
            {
                cronometro.Stop();
            }
            // Después lanzamos el botón de inicio
            Inicio();
        }

        /* Acción que se realiza al hacer click derecho sobre un botón (casilla) del tablero */
        private void Casilla_ClickDerecho(object sender, MouseButtonEventArgs e)
        {

            Button myButton = (Button)sender;
            if ((String)myButton.Content == "")
            {
                // Sólo ponemos banderas si hay banderas disponibles (si quedan minas restantes)
                if (minasRestantes > 0)
                {
                    minasRestantes--;
                    ActualizarMinasRestantes();
                    myButton.Content = EmojiBandera;
                }
                // Si la casilla contiene una bandera, la podemos retirar y aumentamos el número de minas restantes
            }
            else if ((String)myButton.Content == EmojiBandera)
            {
                if (minasRestantes < NumMinas)
                {
                    minasRestantes++;
                    ActualizarMinasRestantes();
                    myButton.Content = "";
                }
            }

        }

        /* Acción que se realiza al hacer click izquierdo sobre un botón (casilla) del tablero */
        private void Casilla_ClickIzquierdo(object sender, RoutedEventArgs e)
        {

            // En caso de que el juego termine, evitamos ejecutar código  
            if (gameOver) return;

            // Botón clickado (obtenemos la posición: fila y columna)
            Button boton = (Button)sender;
            int fila = Grid.GetRow(boton);
            int columna = Grid.GetColumn(boton);

            // Si ya se reveló la casilla, no hacer nada
            if (!boton.IsEnabled)
                return;

            // Incrementamos el número de clicks realizados
            numClicks++;
            // Si el botón contiene una bandera, la "recogemos"
            if ((String)boton.Content == EmojiBandera)
            {
                if (minasRestantes < NumMinas)
                {
                    minasRestantes++;
                    ActualizarMinasRestantes();
                }

            }
            // Contar el número de minas adyacentes
            int minasVecinas = ContarMinasAdyacentes(fila, columna);

            // Comprobamos en la matriz de minas si hay una mina en dicha posición
            if (minas[fila, columna])
            {
                boton.Content = EmojiMina; // Win + V -> Emoji de bomba
                boton.Background = Brushes.Red; // Cambia el color de la casilla a rojo
                TerminarJuego(false);
            }
            else
            {
                // Revelamos la casilla
                boton.IsEnabled = false;
                boton.Background = Brushes.LightGray;

                // Si hay minas vecinas, el contenido de la casilla revelada será dicho número de minas
                if (minasVecinas > 0)
                {
                    // El contenido del botón pasa a ser el número de minas vecinas
                    boton.Content = minasVecinas.ToString();
                    boton.Foreground = ObtenerColorDeNumero(minasVecinas); // Dependiendo del número, tendrá un color
                }
                // En caso contrario, revelamos la casilla actual y seguimos revelando casillas
                else
                {
                    // Revelamos la casilla como "vacía"
                    boton.Content = "";
                    // Seguimos revelando de manera recursiva
                    RevelarCasillasAdyacentes(fila, columna);
                }
                // Sumamos uno al total de casillas reveladas
                casillasReveladas++;

                // Verificar si el juego se ha ganado (si todas las casillas sin minas han sido reveladas)
                // Comprueba que el total de casillas reveladas y el tamaño del tablero menos las minas son iguales
                // (es decir, hemos destapado todo menos las minas)
                if (casillasReveladas == ((Filas * Columnas) - NumMinas))
                {
                    // Termina el juego con win = true (victoria)
                    TerminarJuego(true);
                }
            }

        }

        /* Actualiza el contenido del cronómetro */
        private void Actualizar_Cronometro(object sender, EventArgs e)
        {
            // Primero incrementamos el tiempo en 1 y luego actualizamos el texto del cronómetro
            tiempo++; // Incrementar el tiempo en 1 segundo
            lblCronometro.Content = $"{tiempo:D3}"; // Actualizar el texto del cronómetro y mostrarlo en formato '000' de tres dígitos
        }
    }
}
