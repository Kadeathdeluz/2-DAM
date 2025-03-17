using System.Collections.Generic;

namespace Academia.Data
{
    // Representa un curso de la academia con nombre, duración, nombre del profesor y lista de estudiantes inscritos
    public class Course
    {
        public string CourseName { get; set; }
        public int Duration { get; set; }
        public string ProfessorName { get; set; }
        public List<Student> Students { get; set; }

        // Constructor de la clase Course con parámetros
        public Course(string courseName, int duration, string professorName)
        {
            CourseName = courseName;
            Duration = duration;
            ProfessorName = professorName;
            Students = new List<Student>();
        }

        // Método para añadir un estudiante a la lista de estudiantes del curso
        public void AddStudent(Student student)
        {
            Students.Add(student);
        }

        // Método para eliminar un estudiante de la lista de estudiantes del curso
        public void RemoveStudent(Student student)
        {
            Students.Remove(student);
        }

    }
}
