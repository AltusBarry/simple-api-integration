import React, { Component } from 'react'
import { Container , Form, Row, Col, Button} from 'react-bootstrap'

const axios = require("axios").default;

export default class Create extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      total_health_points: 0,
      armour_class: 0,
    };
    this.handleChange = this.onChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }onChange = (e) => this.setState({ [e.target.name]: e.target.value });handleSubmit(event) {
    axios.post('characters/', {
        name: this.state.emp_regno,
        total_health_points: this.state.emp_name,
        armour_class: this.state.emp_email,
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
    });
    event.preventDefault();
}render() {
  return (
      <Container style={{ marginTop: '100px' }}>
        <h1>Add Employee</h1>
        <Form style={{ margin: '50px' }} >
          <Form.Row>
            <Col>
               <Form.Control placeholder="Employee RegNo" name="emp_regno" value={this.state.emp_regno} onChange={this.onChange}/>
            </Col>
            <Col>
               <Form.Control placeholder="Employee Name" name="emp_name" value={this.state.emp_name} onChange={this.onChange}/>
            </Col>
            <Col>
               <Form.Control placeholder="Employee Email" name="emp_email" value={this.state.emp_email} onChange={this.onChange}/>
            </Col>
            <Col>
               <Form.Control placeholder="Employee Mobile" name="emp_mobile" value={this.state.emp_mobile} onChange={this.onChange}/>
            </Col>
          </Form.Row>
          <Button style={{ margin: '30px', float: 'right' }} onClick={this.handleSubmit}>Add Employee</Button>
       </Form>
     </Container>
      )
   }
}