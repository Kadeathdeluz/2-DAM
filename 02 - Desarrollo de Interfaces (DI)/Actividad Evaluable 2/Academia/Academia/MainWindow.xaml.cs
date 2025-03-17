using Academia.ViewModel;
using System.Windows;

namespace Academia
{

    public partial class MainWindow : Window
    {
        public AcademiaViewModel ViewModel { get; set; }
        public MainWindow()
        {
            InitializeComponent();

            // Inicializar el ViewModel
            ViewModel = new AcademiaViewModel();

            // Pasar el ViewModel al DataContext (para que las pestañas compartan los datos)
            listCoursesFrame.Content = new ListCourses(ViewModel);
            listStudentsFrame.Content = new ListStudents(ViewModel);
            
            createCourseFrame.Content = new CreateCourse(ViewModel);
            createStudentFrame.Content = new CreateStudent(ViewModel);

        }
    }
}