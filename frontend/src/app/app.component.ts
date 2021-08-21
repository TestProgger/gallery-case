import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'my-app';

  constructor() {
    var link:any = document.querySelector("link[rel~='icon']");
    if (!link) {
      link = document.createElement('link');
      link.rel = 'icon';
    }

    if (window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches) {
      link.href = 'favicon_dark.ico';
    } else {
      link.href = 'favicon.ico';
    }

    document.getElementsByTagName('head')[0].appendChild(link);
  }

}
