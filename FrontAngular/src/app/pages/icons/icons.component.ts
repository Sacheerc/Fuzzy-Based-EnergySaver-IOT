import { Component, OnInit } from "@angular/core";
import Chart from 'chart.js';
import { FireService } from 'src/app/services/fire.service';

@Component({
  selector: "app-icons",
  templateUrl: "icons.component.html"
})
export class IconsComponent implements OnInit {

  public canvas : any;
  public ctx;
  public datasets: any;
  public data: any;

  public curr_time: number;
  public curr_light: number;
  public curr_temp: number;

  public timeLineList = [0, 0, 0, 0, 0, 0];
  public lightDataList = [0, 0, 0, 0, 0, 0];
  public tempDataList = [0, 0, 0, 0, 0, 0];

  constructor(private fs: FireService) {
    this.curr_time = 0;
  }

  ngOnInit() {
    this.fs.getCurrentEnv().subscribe((ce: any) => {
      this.curr_light = ce.light;
      this.curr_temp = ce.temperature;
    });

    var gradientChartOptionsConfigurationWithTooltipRed: any = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
  
      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 100,
            suggestedMax: 900,
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }],
  
        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(233,32,16,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }]
      }
    };

    var gradientChartOptionsConfigurationWithTooltipGreen: any = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 2,
            suggestedMax: 6,
            padding: 2,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(0,242,195,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };
  
    // ------------ light power - output chart
    this.canvas = document.getElementById("chartLightPower2");
    this.ctx = this.canvas.getContext("2d");
  
    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);
  
    gradientStroke.addColorStop(1, 'rgba(233,32,16,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(233,32,16,0.0)');
    gradientStroke.addColorStop(0, 'rgba(233,32,16,0)'); //red colors
  
    var data1 = {
      labels: this.timeLineList,
      datasets: [{
        label: "Data",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#ec250d',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#ec250d',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#ec250d',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.lightDataList,
      }]
    };
  
    var myChart1 = new Chart(this.ctx, {
      type: 'line',
      data: data1,
      options: gradientChartOptionsConfigurationWithTooltipRed
    });
    // ------------ light power - output chart
  
    // ------------ temp power - output chart
    this.canvas = document.getElementById("chartTempPower2");
    this.ctx = this.canvas.getContext("2d");
  
  
    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);
  
    gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
    gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
    gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors
  
    var data2 = {
      labels: this.timeLineList,
      datasets: [{
        label: "Data",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.tempDataList,
      }]
    };
  
    var myChart2 = new Chart(this.ctx, {
      type: 'line',
      data: data2,
      options: gradientChartOptionsConfigurationWithTooltipGreen
  
    });
    // ------------ temp power - output chart

    setInterval(()=> {
      this.lightDataList.shift();
      this.lightDataList.push(this.curr_light);
      this.tempDataList.shift();
      this.tempDataList.push(this.curr_temp);
      this.updateTimeLine();
      myChart1.update();
      myChart2.update();
    }, 2000);

  }

  updateTimeLine() {
    if(this.curr_time >= 58) {
      this.curr_time = 0;
    } else {
      this.curr_time += 2;
    }
    this.timeLineList.shift();
    this.timeLineList.push(this.curr_time);
  }
}
