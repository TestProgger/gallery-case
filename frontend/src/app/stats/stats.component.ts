import { Component, OnInit } from '@angular/core';
import { Chart } from 'angular-highcharts';
import { Layout } from '../interfaces/Layout';
import { GalleryService } from '../services/gallery.service'

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.scss']
})
export class StatsComponent implements OnInit {

  public count: number = 10000;
  public layout: Layout[] = [];

  constructor(
    public galleryService: GalleryService
  ) { }

  ngOnInit(){
  }

  chart = new Chart({
    chart: {
      type: 'column'
    },
    title: {
      text: 'График показов билборда по часам'
    },
    credits: {
      enabled: false
    },
    xAxis: {
      categories: [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12',
        '13',
        '14',
        '15',
        '16',
        '17',
        '18',
        '19',
        '20',
        '21',
        '22',
        '23',
        '24',
      ],
      crosshair: true,
      title: {
        text: 'Количество'
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Показы'
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    series: [
      {
        name: 'NVS002APL',
        type: 'column',
        data: [9,9,9,9,9,9,18,18,18,18,18,24,24,18,18,24,24,24,24,18,18,18,9,9]
      }
    ]
  });

  chart1 = new Chart({
    chart: {
        type: 'pie'
    },

    title: {
        text: 'Круговая диаграма'
    },

    subtitle: {
        text: 'Описание'
    },

    tooltip: {
        valueSuffix: '%',
        borderColor: '#8ae'
    },

    series: [{
      name: '% Public',
      colorByPoint: true,
      type: 'pie',
      data: [
        72, 72, 72, 72, 72, 72, 72, 48, 48, 48, 48, 72, 54, 54, 54, 54, 72, 54, 72, 48, 48, 48, 48, 72
    ]
    }]
});

  // add point to chart serie
  add() {
    this.chart.addPoint(Math.floor(Math.random() * 10));
  }

  showCount(){
    this.galleryService.getLayout()
    .subscribe(layout => this.layout = layout);
    console.log(this.layout);
  }

}