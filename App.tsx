import "./global.css";
import React, { useState } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { View, TouchableOpacity, Text } from 'react-native';
import { useCharacterStore } from './src/store/characterStore';
import { CharacterCreation } from './src/screens/CharacterCreation';
import { Dashboard } from './src/screens/Dashboard';
import { Battle } from './src/screens/Battle';

export default function App() {
  const isCreated = useCharacterStore((state) => state.isCreated);
  const [currentScreen, setCurrentScreen] = useState<'dashboard' | 'battle'>('dashboard');

  let content;
  if (!isCreated) {
    content = <CharacterCreation />;
  } else if (currentScreen === 'dashboard') {
    content = (
      <View className="flex-1">
        <Dashboard />
        <View className="px-6 pb-10 bg-slate-950">
          <TouchableOpacity 
            onPress={() => setCurrentScreen('battle')}
            className="w-full bg-blue-600 py-4 rounded-2xl flex-row justify-center items-center shadow-lg shadow-blue-500/30"
          >
            <Text className="text-white font-bold text-lg">Enter Battle Arena</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  } else {
    content = <Battle onBack={() => setCurrentScreen('dashboard')} />;
  }

  // Helper to allow TouchableOpacity and Text inside App.tsx if needed
  // but better to keep it clean. I'll move the button into Dashboard or just keep it simple.
  
  return (
    <SafeAreaProvider>
      <View className="flex-1 bg-slate-950">
        <StatusBar style="light" />
        {isCreated ? (
          currentScreen === 'dashboard' ? (
            <View className="flex-1">
              <Dashboard />
              <View className="absolute bottom-10 left-0 right-0 px-6">
                <TouchableOpacity 
                  onPress={() => setCurrentScreen('battle')}
                  className="w-full bg-blue-600 py-4 rounded-2xl flex-row justify-center items-center shadow-lg shadow-blue-500/30"
                >
                  <Text className="text-white font-bold text-lg">Enter Battle Arena</Text>
                </TouchableOpacity>
              </View>
            </View>
          ) : (
            <Battle onBack={() => setCurrentScreen('dashboard')} />
          )
        ) : (
          <CharacterCreation />
        )}
      </View>
    </SafeAreaProvider>
  );
}
