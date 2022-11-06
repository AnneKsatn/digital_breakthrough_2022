import { Component, OnInit } from '@angular/core';
import { load } from '@2gis/mapgl';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UrlHandlingStrategy } from '@angular/router';
var DG = require('2gis-maps');
import { environment } from 'src/environments/environment';


// const  mapgl


// import { mapgl } from "@googlemaps/js-api-loader"



@Component({
  selector: 'app-system',
  templateUrl: './system.component.html',
  styleUrls: ['./system.component.scss']
})
export class SystemComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  latitude: number = 55.75167;
  longitude: number = 37.61778;
  markers = []
  map: any
  val: any = 0

  cities: any = []
  selectedCities: any[] = [];

  ngOnInit(): void {
    this.map = DG.map('container', {
      'center': [this.latitude, this.longitude],
      'zoom': 13
    });

    var context = this
    this.map.on('moveend', function (e: any) {
      console.log(context.map.getCenter())
    });

    this.cities = [
      { title: 'Северо-Восточный административный округ' },
      { title: 'Восточный административный округ' },
      { title: 'Южный административный округ' },
      { title: 'Центральный административный округ' },
      { title: 'Юго-Восточный административный округ' },
      { title: 'Лукояновский район' },
      { title: 'Романовский район' },
      { title: 'Городской округ Мытищи' },
      { title: 'Западный административный округ' },
      { title: 'Новомосковский административный округ' },
      { title: 'Троицкий административный округ' },


      // { name: 'New York', code: 'NY' },
      // { name: 'Rome', code: 'RM' },
      // { name: 'London', code: 'LDN' },
      // { name: 'Istanbul', code: 'IST' },
      // { name: 'Paris', code: 'PRS' }
    ];
  }

  getExistingRivals() {
    this.httpClient.get(`http://${environment.api}:5000/postmats/rivals`).subscribe((data: any) => {
      console.log(data)

      console.log(data)

      this.markers = data["data"]
      this.markers = this.markers.slice(0, 5)

      this.markers.forEach((coord) => {
        console.log([coord[1], coord[0]])
        DG.marker(
          [coord[0], coord[1]],
          { title: "Постамат конкурент" })
          .addTo(this.map).bindPopup('Постамат конкурент');;
      });
    })
  }

  count() {

    let districts: any = []

    this.selectedCities.forEach(disctict => {
      districts.push(disctict.title)
    })

    console.log(districts)
    console.log(this.val)

    this.httpClient.get(
      `http://${environment.api}:5000/postmats/reccomended?districts[]=${districts}&amount=${this.val}`
    ).subscribe((data: any) => {

      this.map.remove()
      this.map = DG.map('container', {
        'center': [this.latitude, this.longitude],
        'zoom': 13
      });

      const reccomended_postmats = data["data"]

      console.log(reccomended_postmats)

      // this.markers = this.markers.slice(0, 5)

      reccomended_postmats.forEach((postmat: any) => {

        var myIcon = DG.icon({
          iconUrl: 'assets/recloc.png',
          iconSize: [32, 32],
          iconAnchor: [22, 94],
          // className: "icon-recommended"
        });

        DG.marker(
          [postmat[3], postmat[4]],
          { title: "Постамат конкурент", icon: myIcon })
          .addTo(this.map).bindPopup('Постамат конкурент');;
      });
    })
  }
} 
