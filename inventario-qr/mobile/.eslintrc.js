module.exports = {
  root: true,
  extends: ['universe/native', 'plugin:react-hooks/recommended'],
  rules: {
    // Ensures props and state inside functions are always up-to-date
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
};
