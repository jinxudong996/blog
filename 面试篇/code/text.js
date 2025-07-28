function debouce(fn) {
  let timer = null;
  if (timer) clearTimeout(timer);
  timer = setTimeout(() => {
    fn.apply(this, arguments);
  });
}
