# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import streamlit as st

from common import theme

# FUTURE: use localization for international messages

with theme.Theme(autorefresh=False, ephemeral=True):
    # Title
    st.title("Project Dashboard")

    st.write(
        """
    NVIDIA provides example projects to help you get started using NVIDIA AI Workbench for common and advanced tasks.

    Once you have finished the tutorials, feel free to take a look at the following example projects catalog.

    The example projects include the following:
    """
    )

    st.header("NVIDIA Blueprints", divider="gray")

    # Table 0 data
    table0_data = {
        "Blueprint Name": ["PDF-to-Podcast"],
        "Description": ["An example project that PDFs into AI podcasts for engaging on-the-go audio content"],
        "Open in GitHub": ["https://github.com/NVIDIA-AI-Blueprints/pdf-to-podcast"],
        "Open in AI Workbench": [
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS1BSS1CbHVlcHJpbnRzL3BkZi10by1wb2RjYXN0"
        ],
        "Support Forum": [
            "https://forums.developer.nvidia.com/t/support-workbench-example-blueprint-pdf-to-podcast/329784"
        ],
    }

    st.dataframe(
        table0_data,
        column_config={
            "Open in GitHub": st.column_config.LinkColumn("Source Code", display_text="Open in GitHub"),
            "Open in AI Workbench": st.column_config.LinkColumn("Clone and Open", display_text="Open in AI Workbench"),
            "Support Forum": st.column_config.LinkColumn("Developer Forum", display_text="Support Thread"),
        },
        use_container_width=True,
    )

    st.header("Retrieval Augmented Generation (RAG)", divider="gray")

    # Table 1 data
    table1_data = {
        "Project Name": ["Agentic RAG", "Hybrid RAG", "Multimodal Virtual Assistant", "NIM Anywhere"],
        "Description": [
            "An example project for Agentic Retrieval Augmented Generation (RAG)",
            "An example project for Retrieval Augmented Generation (RAG)",
            "An example project to build a multimodal virtual assistant",
            "An example project to accelerate your AI deployment with NVIDIA NIM",
        ],
        "Open in GitHub": [
            "https://github.com/NVIDIA/workbench-example-agentic-rag",
            "https://github.com/NVIDIA/workbench-example-hybrid-rag",
            "https://github.com/NVIDIA/workbench-example-multimodal-virtual-assistant",
            "https://github.com/NVIDIA/nim-anywhere",
        ],
        "Open in AI Workbench": [
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1hZ2VudGljLXJhZw==",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1oeWJyaWQtcmFn",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1tdWx0aW1vZGFsLXZpcnR1YWwtYXNzaXN0YW50",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS9uaW0tYW55d2hlcmU=",
        ],
        "Support Forum": [
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-agentic-rag/303414",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-hybrid-rag/288565",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-multimodal-virtual-assistant/309400",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-nim-anywhere/301001",
        ],
    }

    st.dataframe(
        table1_data,
        column_config={
            "Open in GitHub": st.column_config.LinkColumn("Source Code", display_text="Open in GitHub"),
            "Open in AI Workbench": st.column_config.LinkColumn("Clone and Open", display_text="Open in AI Workbench"),
            "Support Forum": st.column_config.LinkColumn("Developer Forum", display_text="Support Thread"),
        },
        use_container_width=True,
    )

    st.header("Fine-tuning Models", divider="gray")

    # Table 2 data
    table2_data = {
        "Project Name": [
            "Llama 2 Finetune",
            "Llama 3 8b Finetune",
            "Mistral Finetune",
            "Mixtral 8x7b Finetune",
            "NeMo Ptuning",
            "NeMo Punctuation",
            "Nemotron Finetune",
            "Phi-3 Mini Finetune",
            "SDXL Customization",
        ],
        "Description": [
            "An example project to fine-tune Llama 2",
            "An example project to fine-tune a Llama 3 8B Model",
            "An example project to fine-tune a Mistral 7B model",
            "An example project to fine-tune a Mixtral 8x7B Model",
            "An example project to p-tune LLMs with NeMo Framework",
            "An example project to annotate text with NeMo Framework",
            "An example project to fine-tune a Nemotron-3 8B model",
            "An example project to fine-tune a Phi-3 Mini Model",
            "An example project to customize an SDXL model",
        ],
        "Open in GitHub": [
            "https://github.com/NVIDIA/workbench-example-llama2-finetune",
            "https://github.com/NVIDIA/workbench-example-llama3-finetune",
            "https://github.com/NVIDIA/workbench-example-mistral-finetune",
            "https://github.com/NVIDIA/workbench-example-mixtral-finetune",
            "https://github.com/NVIDIA/workbench-example-nemo-ptuning",
            "https://github.com/NVIDIA/workbench-example-nemo-punctuation",
            "https://github.com/NVIDIA/workbench-example-nemotron-finetune",
            "https://github.com/NVIDIA/workbench-example-phi3-finetune",
            "https://github.com/NVIDIA/workbench-example-sdxl-customization",
        ],
        "Open in AI Workbench": [
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1sbGFtYTItZmluZXR1bmU=",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1sbGFtYTMtZmluZXR1bmU=",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1taXN0cmFsLWZpbmV0dW5l",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1taXh0cmFsLWZpbmV0dW5l",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1uZW1vLXB0dW5pbmc=",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1uZW1vLXB1bmN0dWF0aW9u",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1uZW1vdHJvbi1maW5ldHVuZQ==",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1waGkzLWZpbmV0dW5l",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1zZHhsLWN1c3RvbWl6YXRpb24=",
        ],
        "Support Forum": [
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-llama-2-finetune/278375",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-llama-3-finetune/303411",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-mistral-finetune/278376",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-mixtral-finetune/303413",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-nemo-p-tuning/278370",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-nemo-punctuation/278371",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-nemotron-finetune/278377",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-phi-3-finetune/303412",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-sdxl-customization/278374",
        ],
    }

    st.dataframe(
        table2_data,
        column_config={
            "Open in GitHub": st.column_config.LinkColumn("Source Code", display_text="Open in GitHub"),
            "Open in AI Workbench": st.column_config.LinkColumn("Clone and Open", display_text="Open in AI Workbench"),
            "Support Forum": st.column_config.LinkColumn("Developer Forum", display_text="Support Thread"),
        },
        use_container_width=True,
    )

    st.header("Data Science Workflows", divider="gray")

    # Table 3 data
    table3_data = {
        "Project Name": ["Competition Kernel", "RAPIDS CuDF", "RAPIDS CuML"],
        "Description": [
            "An example project to bring your own compute to any Kaggle competition",
            "An example project to explore the RAPIDS cuDF library",
            "An example project to explore the RAPIDS cuML library",
        ],
        "Open in GitHub": [
            "https://github.com/NVIDIA/workbench-example-competition-kernel",
            "https://github.com/NVIDIA/workbench-example-rapids-cudf",
            "https://github.com/NVIDIA/workbench-example-rapids-cuml",
        ],
        "Open in AI Workbench": [
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1jb21wZXRpdGlvbi1rZXJuZWw=",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1yYXBpZHMtY3VkZg==",
            "https://ngc.nvidia.com/open-ai-workbench/aHR0cHM6Ly9naXRodWIuY29tL05WSURJQS93b3JrYmVuY2gtZXhhbXBsZS1yYXBpZHMtY3VtbA==",
        ],
        "Support Forum": [
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-competition-kernel/309399",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-rapids-cudf/278372",
            "https://forums.developer.nvidia.com/t/support-workbench-example-project-rapids-cuml/278373",
        ],
    }

    st.dataframe(
        table3_data,
        column_config={
            "Open in GitHub": st.column_config.LinkColumn("Source Code", display_text="Open in GitHub"),
            "Open in AI Workbench": st.column_config.LinkColumn("Clone and Open", display_text="Open in AI Workbench"),
            "Support Forum": st.column_config.LinkColumn("Developer Forum", display_text="Support Thread"),
        },
        use_container_width=True,
    )
