import createApp from './createApp'

export default context => {
    const { app } = createApp(context);
    return app;
}