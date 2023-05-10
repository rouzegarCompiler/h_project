const template = document.createElement('template');

template.innerHTML = `
    <div class="rules_container">
        <table class="rounded">
            <tr>
                <th>تعرفه</th>
                <th>5000 دلار</th>
                <th>10000 دلار</th>
                <th>25000 دلار</th>
                <th>50000 دلار</th>
            </tr>
            <tr>
                <td>سود مرحله اول</td>
                <td>400$</td>
                <td>800$</td>
                <td>2000$</td>
                <td>4000$</td>
            </tr>
            <tr>
                <td>سود مرحله دوم</td>
                <td>200$</td>
                <td>400$</td>
                <td>1000$</td>
                <td>2000$</td>
            </tr>
`;

document.body.appendChild(template.content);