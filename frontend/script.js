document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/api/data")
    .then(response => response.json())
    .then(data => {
      // Set basic info
      document.getElementById("fullname").textContent = ` ${data.student_name}`;
      document.getElementById("student_id").textContent = ` ${data.student_id}`;
      document.getElementById("year_of_entry").textContent = ` ${data.entry_year}`;

      const transcriptContainer = document.getElementById("transcript-container");

      data.semesters.forEach(semester => {
        let semesterHTML = `
          <div class="overflow-x-auto mb-6">
            <table class="w-full table-auto border border-gray-300 text-sm">
              <caption class="caption-top text-center font-semibold py-1 bg-black text-white">${semester.name}</caption>
              <thead class="bg-gray-200">
                <tr>
                  <th class="border px-2 py-1">Code</th>
                  <th class="border px-2 py-1">Name</th>
                  <th class="border px-2 py-1">Grade</th>
                  <th class="border px-2 py-1">Cr</th>
                </tr>
              </thead>
              <tbody>
        `;

        semester.courses.forEach(course => {
          semesterHTML += `
            <tr>
              <td class="border px-2 py-1">${course.code}</td>
              <td class="border px-2 py-1">${course.name}</td>
              <td class="border px-2 py-1">${course.grade}</td>
              <td class="border px-2 py-1">${course.credit}</td>
            </tr>
          `;
        });

        semesterHTML += `
            <tr><td colspan="4" class="border px-2 py-1 text-center">--------------------</td></tr>
            <tr>
              <td colspan="2" class="border px-2 py-1 font-semibold">GPA</td>
              <td class="border px-2 py-1">${semester.gpa}</td>
              <td class="border px-2 py-1">${semester.total_credits}</td>
            </tr>
            <tr>
              <td colspan="2" class="border px-2 py-1 font-semibold">CGPA</td>
              <td class="border px-2 py-1">${semester.cgpa || data.cgpa || '-'}</td>
              <td class="border px-2 py-1">${semester.total_credits}</td>
            </tr>
          </tbody>
        </table>
      </div>
        `;

        transcriptContainer.innerHTML += semesterHTML;
      });
    })
    .catch(error => {
      console.error("Error fetching data:", error);
    });
});

