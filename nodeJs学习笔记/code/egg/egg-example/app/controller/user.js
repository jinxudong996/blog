'use strict';

const Controller = require('egg').Controller;

class UserController extends Controller{
  async index(){
    const {ctx} = this;

    ctx.body = 'user index'
  }

  async lists(){
    const {ctx} = this;
    await new Promise(resolve => {
      setTimeout(() => {
        resolve()
      }, 500);
    })
    ctx.body = 'hello user/lists'
  }

  async detail(){
    const { ctx } = this;
    ctx.body = ctx.query;
  }

  async detail2(){
    const { ctx } = this;
    ctx.body = ctx.query;
  }

  async add() {
    const { ctx } = this;

    const rule = {
      name: { type: 'string' },
      age: { type: 'number' },
    };
    ctx.body = {
      status: 200,
      data: ctx.request.body,
    };
  }


}

module.exports = UserController