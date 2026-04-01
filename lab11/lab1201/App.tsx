import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider } from 'react-redux';
import { store } from './src/store';
import { NotesListScreen, AddNoteScreen, NoteDetailScreen } from './src/screens';
import { initDatabase } from './src/utils/database';
import { View, Text, ActivityIndicator, Alert } from 'react-native';

const Stack = createStackNavigator();

export default function App() {
    const [isReady, setIsReady] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        initDatabase()
            .then(() => {
                setIsReady(true);
            })
            .catch(error => {
                console.error(error);
                setError('Не удалось инициализировать базу данных');
                Alert.alert('Ошибка', 'Не удалось инициализировать базу данных');
            });
    }, []);

    if (!isReady) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <ActivityIndicator size="large" color="#007AFF" />
                <Text style={{ marginTop: 20 }}>Загрузка...</Text>
            </View>
        );
    }

    if (error) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text style={{ color: 'red', fontSize: 18, marginBottom: 20 }}>{error}</Text>
                <Text>Пожалуйста, перезапустите приложение</Text>
            </View>
        );
    }

    return (
        <Provider store={store}>
            <NavigationContainer>
                <Stack.Navigator
                    initialRouteName="NotesList"
                    screenOptions={{
                        headerStyle: {
                            backgroundColor: '#007AFF'
                        },
                        headerTintColor: 'white',
                        headerTitleStyle: {
                            fontWeight: 'bold'
                        }
                    }}
                >
                    <Stack.Screen
                        name="NotesList"
                        component={NotesListScreen}
                        options={{ title: 'Гео-заметки' }}
                    />
                    <Stack.Screen
                        name="AddNote"
                        component={AddNoteScreen}
                        options={{ title: 'Новая заметка' }}
                    />
                    <Stack.Screen
                        name="NoteDetail"
                        component={NoteDetailScreen}
                        options={{ title: 'Детали заметки' }}
                    />
                </Stack.Navigator>
            </NavigationContainer>
        </Provider>
    );
}
