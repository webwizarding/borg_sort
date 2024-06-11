fetch('sorted_ages.csv')
    .then(response => response.text())
    .then(data => {
        const tableBody = document.querySelector('#ageTable tbody');
        const rows = data.split('\n').slice(1); // Skip header row
        rows.forEach((row, index) => {
            const cols = row.split(',');
            if (cols.length >= 2) {
                const tr = document.createElement('tr');
                const indexTd = document.createElement('td');
                const ageTd = document.createElement('td');
                const genderTd = document.createElement('td');
                indexTd.textContent = index + 1;
                ageTd.textContent = cols[0];
                genderTd.textContent = cols[1];
                tr.appendChild(indexTd);
                tr.appendChild(ageTd);
                tr.appendChild(genderTd);
                tableBody.appendChild(tr);
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));
