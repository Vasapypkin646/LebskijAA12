package com.example.notesapp.ui

import com.example.notesapp.ui.EditNoteViewModel
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEditNoteScreen(
    viewModel: EditNoteViewModel,
    onNavigateBack: () -> Unit
) {
    val note by viewModel.note.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()

    var title by remember { mutableStateOf("") }
    var content by remember { mutableStateOf("") }

    // Обновляем поля, когда загрузится заметка (только для редактирования)
    LaunchedEffect(note) {
        if (note != null) {
            title = note!!.title
            content = note!!.content
        }
    }

    // Если ошибка загрузки, показываем сообщение и кнопку назад
    if (error != null) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(error!!, color = MaterialTheme.colorScheme.error)
                Spacer(modifier = Modifier.height(8.dp))
                Button(onClick = onNavigateBack) { Text("Назад") }
            }
        }
        return
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (note != null) "Редактирование" else "Новая заметка") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Назад")
                    }
                },
                actions = {
                    TextButton(
                        onClick = {
                            if (title.isNotBlank() && content.isNotBlank()) {
                                viewModel.saveNote(title, content) {
                                    onNavigateBack()
                                }
                            }
                        },
                        enabled = title.isNotBlank() && content.isNotBlank()
                    ) {
                        Text("Сохранить")
                    }
                }
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            if (isLoading) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            } else {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    OutlinedTextField(
                        value = title,
                        onValueChange = { title = it },
                        label = { Text("Заголовок") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )

                    OutlinedTextField(
                        value = content,
                        onValueChange = { content = it },
                        label = { Text("Содержание") },
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f),
                        minLines = 5
                    )
                }
            }
        }
    }
}