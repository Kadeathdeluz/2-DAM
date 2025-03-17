using System.Collections.Generic;

namespace Academia.Data
{
    // Representa un estudiante de la academia con nombre, apellido, edad y lista de cursos inscritos
    public class Student
    {
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public int Age { get; set; }
        public List<Course> Courses { get; set; } = new List<Course>();

        // Constructor de la clase Student con parámetros
        public Student(string firstName, string lastName, int age)
        {
            FirstName = firstName;
            LastName = lastName;
            Age = age;
            Courses = new List<Course>();
        }

        // Método para añadir un curso a la lista de cursos del estudiante
        public void AddCourse(Course course)
        {
            Courses.Add(course);
        }

        // Método para eliminar un curso de la lista de cursos del estudiante
        public void RemoveCourse(Course course)
        {
            Courses.Remove(course);
        }
    }
}
