const { getDefaultConfig } = require('expo/metro-config');

module.exports = (async () => {
    const config = await getDefaultConfig(__dirname);
    
    // Добавляем поддержку веб-заглушек
    config.resolver.extraNodeModules = {
        ...config.resolver.extraNodeModules,
        'react-native-maps': __dirname + '/src/web/react-native-maps.web.ts',
    };
    
    return config;
})();
