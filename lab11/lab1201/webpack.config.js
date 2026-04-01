const createExpoWebpackConfigAsync = require('@expo/webpack-config');

module.exports = async function (env, argv) {
    const config = await createExpoWebpackConfigAsync(env, argv);
    
    // Заменяем react-native-maps на заглушку для веба
    config.resolve.alias = {
        ...config.resolve.alias,
        'react-native-maps': require.resolve('./src/web/react-native-maps.web.ts'),
    };
    
    return config;
};