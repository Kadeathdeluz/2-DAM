using Academia.Data;
using System.Collections.ObjectModel;
using System.ComponentModel;

namespace Academia.ViewModel
{
    // Clase que representa el ViewModel de la aplicación (para compartir datos entre las vistas con una arquitecura MVVM)
    public class AcademiaViewModel : INotifyPropertyChanged
    {
        private ObservableCollection<Student> _students;
        private ObservableCollection<Course> _courses;

        // Propiedad (Estudiantes)
        public ObservableCollection<Student> Students
        {
            get => _students;
            set
            {
                _students = value;
                OnPropertyChanged(nameof(Students));
            }
        }
        // Propiedad (Cursos)
        public ObservableCollection<Course> Courses
        {
            get => _courses;
            set
            {
                _courses = value;
                OnPropertyChanged(nameof(Courses));
            }
        }

        // El ViewModel se crea con datos de ejemplo
        public AcademiaViewModel()
        {
            // Basta con comentar las llamadas para que no se inicialicen los datos de prueba y las listas queden vacías
            InitializeStudents();

            InitializeCouses();

        }

        public event PropertyChangedEventHandler PropertyChanged;

        // Método para notificar a la vista que una propiedad ha cambiado
        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        // Método para inicializar la lista de estudiantes con datos de prueba
        private void InitializeStudents()
        {
            // Creamos varios estudiantes como datos de prueba
            Students = new ObservableCollection<Student>
            {
                new Student
                (
                    "Ernesto",
                    "Anastasio",
                    27
                 ),

                new Student
                (
                    "Albus",
                    "Dumbledore",
                    100
                ),
                new Student
                (
                    "Jesu",
                    "Cristus",
                    33
                ),
                new Student
                (
                    "R2",
                    "D2",
                    18
                )
            };
            // Creamos otro estudiante como dato de prueba
            Student otherStudent = new Student
            (
                "Obi-Wan",
                "Kenobi",
                57
            );
            // Le añadimos un curso al estudiante para probar que no se muestra en la lista de estudiantes
            otherStudent.AddCourse(new Course("The Force", 100, "Yoda"));
            // Añadimos el estudiante a la lista de estudiantes
            Students.Add(otherStudent);
        }

        //Método para inicializar la lista de cursos con datos de prueba
        private void InitializeCouses()
        {
            // Creamos varios cursos como datos de prueba
            Courses = new ObservableCollection<Course>
            {
                new Course("The Force", 100, "Yoda"),
                new Course("Defense Against the Dark Arts", 50, "Severus Snape"),
                new Course("Transfiguration", 50, "Minerva McGonagall"),
                new Course("Flying", 50, "Madam Hooch"),
                new Course("Muggle Studies", 50, "Charity Burbage"),
            };
            // Creamos otro curso como dato de prueba
            Course otherCourse = new Course("Inventología", 10, "Mao Tse Tung");

            // Le añadimos un estudiante al curso para probar que no se muestra en la lista de cursos
            otherCourse.AddStudent(new Student("Charlie", "Los Ángeles", 20));
            // Añadimos el curso a la lista de cursos
            Courses.Add(otherCourse);

        }
    }
}