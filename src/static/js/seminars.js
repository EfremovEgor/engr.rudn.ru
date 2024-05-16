const url = window.location.pathname;
const id = url.substring(url.lastIndexOf("/") + 1);
const months = [
  "Январь",
  "Февраль",
  "Март",
  "Апрель",
  "Май",
  "Июнь",
  "Июль",
  "Август",
  "Сентябрь",
  "Октябрь",
  "Ноябрь",
  "Декабрь",
];

function generateEmptyContent(data) {
  let content = new Map();

  for (
    let year = data["dates"]["year_start"];
    year <= data["dates"]["year_end"];
    year++
  )
    months.forEach((month, i) => {
      {
        if (year == data["dates"]["year_start"]) {
          if (i + 1 < data["dates"]["month_start"]) {
            return;
          }
        }
        if (year == data["dates"]["year_end"]) {
          if (i + 1 > data["dates"]["month_end"]) {
            return;
          }
        }
        let weeks = new Map();
        for (let week = 1; week <= 5; week++) {
          weeks.set(week, []);
        }
        content.set(
          `${month.charAt(0).toUpperCase() + month.slice(1)} ${year}`,
          weeks
        );
      }
    });
  return content;
}
function populateContent(content, data) {
  let fifth_week = false;
  for (const report of Object.values(data["reports"])) {
    const date = new Date(report["date_start"]);
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    if (report["week"] == 5) {
      fifth_week = true;
    }
    content
      .get(`${month.charAt(0).toUpperCase() + month.slice(1)} ${year}`)
      .get(report["week"])
      .push(report);
  }
  return fifth_week;
}
function generateTable(data) {
  let content = generateEmptyContent(data);
  const fifthWeek = populateContent(content, data);
  let tableHeading = "";
  let table = "";
  const currentMonth = months[new Date().getMonth()];
  const currentYear = new Date().getFullYear();
  const currentMonthYear = `${
    currentMonth.charAt(0).toUpperCase() + currentMonth.slice(1)
  } ${currentYear}`;
  console.log(data);
  content.forEach((weeks, key) => {
    tableHeading += `<div>${key}</div>`;
    let monthlyItems = "";
    weeks.forEach((reports, weekIndex) => {
      let weeklyItems = "";
      reports.forEach((report, reportIndex) => {
        weeklyItems += `
        <div href="/science/seminars/${id}/reports/${report.id}" class="report">
          <div class="badge-container">
            <span class="uk-badge">${new Date(
              report.date_start
            ).toLocaleDateString()} ${report.time_start
          .split(":")
          .slice(0, 2)
          .join(":")}
            </span>
          </div>
          <h4>Название доклада:</h4>
          <span class="report-info">${report.name}</span>
          <h4>Докладчик:</h4>
          <span class="report-info">${report.speaker.first_name} ${
          report.speaker.last_name
        },  ${report.speaker.job_title[0]},  ${
          report.speaker.academic_degree
        }</span>
          
        </div>`;
      });
      if (weekIndex == 5 && !fifthWeek) {
        return;
      }
      monthlyItems += `<div class="weekly_reports">${weeklyItems}</div>`;
    });
    if (key !== currentMonthYear) {
      table += `<div class="monthly_reports">${monthlyItems}</div>`;
    } else {
      table += `<div id="scrollTo" class="monthly_reports">${monthlyItems}</div>`;
    }
  });
  table = `<div class="reports-body">${table}</div>`;
  $("#time").html(tableHeading);
  $("#reports").append(table);
  document
    .getElementById("scrollTo")
    .scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
  $(".report").click((element) => {
    window.location.href = $(element.currentTarget).attr("href");
  });
}

$(document).ready(function () {
  $.get(`/science/seminar/${id}/get_reports`, function (content) {
    const data = content;
    generateTable(data);
  });
});
