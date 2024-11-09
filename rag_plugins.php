<?php
/*
Plugin Name: RAG Chatbot Embedder
Description: Embeds the Python-based RAG chatbot.
Version: 1.0
Author: Your Name
*/

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly.
}

// Enqueue frontend script
function rag_chatbot_enqueue_scripts() {
    wp_enqueue_script('rag-chatbot-widget', plugin_dir_url(__FILE__) . 'chatbot-widget.js', array('jquery'), '1.0', true);
}
add_action('wp_enqueue_scripts', 'rag_chatbot_enqueue_scripts');

// Add chatbot container to the footer
function rag_chatbot_render_widget() {
    echo '<div id="rag-chatbot-container"></div>';
}
add_action('wp_footer', 'rag_chatbot_render_widget');
?>
