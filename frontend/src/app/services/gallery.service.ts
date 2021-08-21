import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Layout } from '../interfaces/Layout'


@Injectable({ providedIn: 'root' })
export class GalleryService {

  private showUrl = 'api/one';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient) { }

  /** GET layout from the server */
  getLayout(): Observable<Layout[]> {
    return this.http.get<Layout[]>(this.showUrl)
      .pipe(
        tap(_ => console.log('err'))
      );
  }

}