import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginFormComponent } from './login-form.component';

describe('LoginFormComponent', () => {
  let fixture: ComponentFixture<LoginFormComponent>;
  let component: LoginFormComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [LoginFormComponent],
    });

    fixture = TestBed.createComponent(LoginFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should emit submitted event when form valid', () => {
    spyOn(component.submitted, 'emit');

    component.form.setValue({ email: 'user@test.com', password: 'secret123' });
    component.onSubmit();

    expect(component.submitted.emit).toHaveBeenCalledWith({ email: 'user@test.com', password: 'secret123' });
  });

  it('should not submit when form invalid', () => {
    spyOn(component.submitted, 'emit');

    component.form.setValue({ email: 'invalid', password: '123' });
    component.onSubmit();

    expect(component.submitted.emit).not.toHaveBeenCalled();
  });
});
