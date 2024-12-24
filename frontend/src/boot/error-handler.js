// src/boot/error-handler.js
export default ({ app }) => {
  // Глобальный обработчик ошибок Vue
  app.config.errorHandler = (err, vm, info) => {
    console.error('Vue Error:', err);
    console.error('Error Info:', info);
  };
};
