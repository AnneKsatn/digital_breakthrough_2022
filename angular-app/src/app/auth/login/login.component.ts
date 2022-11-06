import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  form: FormGroup = new FormGroup({
    'email': new FormControl('', Validators.email),
    'password': new FormControl('', Validators.minLength(5))
  });

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private httpClient: HttpClient
  ) { }

  ngOnInit(): void {
  }

  onSubmit() {
    console.log(this.form.value.email)
    console.log(this.form.value.password)

    this.httpClient.get(
      `http://${environment.api}:5000/login?login=${this.form.value.email}&pass=${this.form.value.password}`).subscribe((data: any) => {
        if (data == true) {
          this.router.navigateByUrl("system/home-page")
        }
      })
  }

  registration() {
    this.router.navigateByUrl("/registration")
  }

  loginLogistCompany() {

  }

}
