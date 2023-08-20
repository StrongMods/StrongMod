#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <windows.h>

#define JMP_CODE_SIZE 5


char* generate_jump_near_machine_code(void* target_address, void* instruction_location) {
    static char machine_code[5];
    machine_code[0] = 0xE9;
    *(int*)(machine_code + 1) = (int)(target_address) - ((int)instruction_location + 5);
    return machine_code;
}


void set_memory_permission(int memory, size_t code_size, int protection_flags) {
    DWORD oldProtect;
    VirtualProtect((void *)memory, code_size, protection_flags, &oldProtect);
}

void hook_at(int address, void* function) {
    char* jump_code = generate_jump_near_machine_code((void*)function, (void*)address);;
    set_memory_permission(address, JMP_CODE_SIZE, PAGE_EXECUTE_READWRITE);
    memcpy((void*)address, jump_code, JMP_CODE_SIZE);
}
// game tick
typedef void (*HandleGameTickEvent)(void);

HandleGameTickEvent handle_game_tick_event;

void game_tick_hook_handler() {
    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");

    handle_game_tick_event();
    // restore registers
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");
    // execute stole code
    asm ("mov eax,[0x1FE7D78];");
    // back to normal path
    asm ("leave;");
    asm ("jmp 0x045CC81");
}

void execute_callback_on_game_tick(HandleGameTickEvent function) {
    handle_game_tick_event = function;
    hook_at(0x045CC7C, (void*)game_tick_hook_handler);
}

// ui tick
typedef void (*HandleUITickEvent)(void);

HandleUITickEvent handle_ui_tick_event;

void ui_tick_hook_handler() {
    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");
    asm ("push esi;");

    handle_ui_tick_event();
    // restore registers
    asm ("pop esi;");
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");

    // back to normal path 1
    asm ("leave;");

    // execute stole code
    asm ("cmp edi,ebp;");
    asm ("mov [esi+0x00001E0],eax;");

    // back to normal path 2
    asm ("jmp 0x04700fc;");
}

void execute_callback_on_ui_tick(HandleUITickEvent function) {
    handle_ui_tick_event = function;
    hook_at(0x04700F4, (void*)ui_tick_hook_handler);
}

typedef struct {
    char *context;
    int player;
} Message;

void get_last_message(Message *last_message) {
    char *context = (char *)((0x1A1F33A) + ((int)(*((int *)0x1A22DD4)) * 0xFA));
    int *player = (int *)((0x1A22DE0) + ((int)(*((int *)0x1A22DD4)) * 0x10));
    last_message->context = context;
    last_message->player = *player;
}

void enable_chat() {
    char jmp = 0xEB;
    set_memory_permission(0x04B30E4, 1, PAGE_EXECUTE_READWRITE);
    *(char *)(0x04B30E4) = jmp;
    set_memory_permission(0x04B3193, 1, PAGE_EXECUTE_READWRITE);
    *(char *)(0x04B3193) = jmp;
    short nops = 0x9090;
    set_memory_permission(0x04b3172, 2, PAGE_EXECUTE_READWRITE);
    *(short *)(0x04b3172) = nops;
}


void send_message(char* name, char* message) {
    asm("mov eax,0x0000000;"
        "mov ebx,0x000000E;"
        "mov ecx,0x191D768;"
        "mov edx,0x0000001;"
        "push 0x00;"
        "push 0x01;"
        "call 1f;"
        "jmp end;"
        "1:;"
        "push ebx;"
        "push esi;"
        "mov esi,ecx;"
        "add dword ptr [esi+0x010566C],01;"
        "mov eax,[esi+0x010566C];"
        "cmp eax,0x14;"
        "push edi;"
        "jl 2f;"
        "mov dword ptr [ESI + 0x10566c],0x0;"
        "2:;"
        "mov eax,[esi+0x010566C];"
        "mov edi,[esp+0x10];"
        "shl eax,0x04;"
        "mov [eax+esi+0x0105678],edi;"
        "call dword ptr [0x059E228];"
        "mov ecx,[esi+0x010566C];"
        "mov ebx,[esp+0x14];"
        "shl ecx,0x04;"
        "mov [ecx+esi+0x010567C],eax;"
        "mov edx,[esi+0x010566C];"
        "add edx,0x0010568;"
        "shl edx,0x04;"
        "mov dword ptr [EDX + ESI*0x1],0x1;"
        "mov eax,[esi+0x010566C];"
        "shl eax,0x04;"
        "mov [eax+esi+0x0105684],ebx;"
        "mov ecx,[esi+0x010566C];"
        "imul ecx,ecx,0x00000FA;"
        "lea edx,[ecx+esi+0x0101BD2];"
        "push edx;"
        "lea eax,[esi+0x0101AD8];");
    asm("push eax;"
        "push 0x00000FA;"
        "mov ecx,0x165272C;"
        "call 0x0471830;"
        "test edi,edi;"
        "mov ecx,[esi+0x010566C];"
        "imul ecx,ecx,0x00000FA;"
        "lea edx,[ecx+esi+0x0102F5A];"
        "push edx;"
        "push 0x07;"
        "push 0x4C;"
        "mov ecx,0x2157578;"
        "call 0x046A050;" : : "r"(message));
    asm("push eax;"
        "push 0x00000FA;"
        "mov ecx,0x165272C;"
        "call 0x0471830;"
        "pop edi;"
        "mov dword ptr [ESI + 0x1072f0],0x0;"
        "pop esi;"
        "pop ebx;"
        "ret 0x008;"
        "end:;": : "r"(name));
}


void train_unit(int player, int unit) {
    asm("push 0x0;"
        "push eax;"
        "push 0x16;"
        "push edx;"
        "mov ecx, 0x1387F38;"
        "mov edx, 0x0000001;"
        "call 0x052ec10;": : "r"(player), "r"(unit));
}


void move_units(int* units, int size, int x, int y) {
    int group_id;
    for (int i = 0; i < size; i++) {
        asm("mov ecx, 0x23FC8E8;"
            "push 0x16;"
            "push eax;"
            "call grouping_units;"
            "jmp l2;"
            "grouping_units:"
            "push esi;"
            "push edi;"
            "mov edi,[esp+0xC];"
            "mov eax,edi;"
            "imul eax,eax,0x0000490;"
            "movsx edx,word ptr [eax+0x13885E2];"
            "mov esi,edx;"
            "imul esi,esi,0x00039F4;"
            "cmp dword ptr [esi+0x115E0F8],0x00;"
            "mov esi,[esp+0x10];"
            "push esi;"
            "push edi;"
            "push edx;"
            "mov [eax+0x1388976],si;"
            "call l3;"
            "push eax;"
            "test eax,eax;"
            "push eax;"
            "push edi;"
            "mov ecx,0x1667F78;"
            "call 0x0522590;"
            "l1:"
            "pop eax;"
            "pop edi;"
            "pop esi;"
            "ret 0x008;"
            "l3:"
            "sub esp,0x8;"
            "push ebx;"
            "mov ebx,[esp+0x10];"
            "mov eax,ebx;"
            "imul eax,eax,0x00039F4;"
            "mov eax,[eax+0x115E0F8];"
            "test eax,eax;"
            "jmp 0x04CCD41;"

            "l2:"
            :  "=r" (group_id) : "r"(units[i]));
    }

    asm("push 0x0;"
        "push edx;"
        "push ecx;"
        "push eax;"
        "mov ecx, 0x1667F78;"
        "call 0x0526f00;" : : "r"(group_id), "r"(x), "r"(y));

    for (int i = 0; i < size; i++) {
        asm("mov ecx, 0x23FC8E8;"
            "push 0x11;"
            "push eax;"
            "call grouping_units_2;"
            "jmp l2_2;"
            "grouping_units_2:"
            "push esi;"
            "push edi;"
            "mov edi,[esp+0xC];"
            "mov eax,edi;"
            "imul eax,eax,0x0000490;"
            "movsx edx,word ptr [eax+0x13885E2];"
            "mov esi,edx;"
            "imul esi,esi,0x00039F4;"
            "cmp dword ptr [esi+0x115E0F8],0x00;"
            "mov esi,[esp+0x10];"
            "push esi;"
            "push edi;"
            "push edx;"
            "mov [eax+0x1388976],si;"
            "call l3_2;"
            "push eax;"
            "test eax,eax;"
            "push eax;"
            "push edi;"
            "mov ecx,0x1667F78;"
            "call 0x0522590;"
            "l1_2:"
            "pop eax;"
            "pop edi;"
            "pop esi;"
            "ret 0x008;"
            "l3_2:"
            "sub esp,0x8;"
            "push ebx;"
            "mov ebx,[esp+0x10];"
            "mov eax,ebx;"
            "imul eax,eax,0x00039F4;"
            "mov eax,[eax+0x115E0F8];"
            "test eax,eax;"
            "jmp 0x04CCD41;"

            "l2_2:"
            : : "r"(units[i]));
    }

}

void place_wall(int lord_id, int x, int y) {
    asm("push 0x19;"
        // location
        "push edx;"
        "push ecx;"
        // player
        "push eax;"
        "mov ecx, 0x1A93208;"
        "call 0x05034A0;": : "r"(lord_id), "r"(x), "r"(y));
}


int get_unit_owner(int unit) {
    int lord_id;

    asm("mov ebx, 0x490;"
        "imul ebx, [%1];"
        "mov ebx, [0x1388A5C+ebx];"
        "mov [%0], ebx;" : "=m" (lord_id) : "m"(unit));
    return lord_id;
}

int is_game_loaded() {
    int is_loaded;
    asm("mov eax, [0x0F2C9BC];": "=r" (is_loaded) : :);
    return is_loaded;
}

void set_game_speed(int speed) {
    asm("mov [0x1FE7DD8], eax;": : "r"(speed):);
}

void zoom_in() {
    asm("mov dword ptr [0x21AEC68], 0;": : :);
}

void zoom_out() {
    asm("mov dword ptr [0x21AEC68], 1;": : :);
}


int get_buying_price(int player_id, int good_id, int number_of_goods) {
    int price;
    asm(// number of goods
        "push [%1];"
        // good id
        "push [%2];"
        // player id
        "push [%3];"
        "mov ecx, 0x112B0B8;"
        "call 0x04588A0;": "=a"(price): "m"(number_of_goods), "m"(good_id), "m"(player_id));
    return price;
}


void place_building(int player_id, int building_id, int x, int y) {
    asm(
        // mode number(is wall behind it) if there is only one mode it should be F
        "push 0xF;"
        // get number of blocks it takes
        "push %1;"
        "call 0x04fa550;"
        // number of blocks it takes
        "push eax;"
        // item
        "push %1;"
        // location
        "push %2;"
        "push %3;"

        // player_id
        "push %0;"

        "mov ebx, 0x1A27654;"
        "mov ecx, 0x1A93208;"
        "mov edx, 0x0000001;"
        "mov esi, 0x0000000;"
        "mov edi, 0x0000000;"

        "call 0x05162d0;": : "m"(player_id), "m"(building_id), "m"(x), "m"(y));
}

int is_iron_ore(int x, int y) {
    int this = 0x1A93208;
    int uVar1;
    int* ptr = (int*)0x2337300;
    int iVar4;
    int uVar3;


    uVar1 = x;
    uVar3 = y;


    iVar4 = ptr[uVar3 * 3] + x;

    uVar1 = *(unsigned int *)(this + 0x165160 + iVar4 * 4);

    if ((uVar1 & 0x80000) != 0) {
      return 1;
    }
    return 0;
}


int is_unit_exist(int unit) {
    int exist;

    asm("mov eax, 0x490;"
        "mov ebx, %1;"
        "imul eax, ebx;"
        "mov %0, [0x1388A68+eax];": "=r" (exist) : "m"(unit));
    if (exist!=0) {
        return 1;
    }
    return 0;
}

int get_unit_id(int unit) {
    int unit_id;

    asm("mov eax, 0x490;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov %0, [0x1388A74+eax];" : "=r" (unit_id) : "m"(unit));
    return unit_id;
}


typedef struct {
    int index;
    int id;
} BuildingIndexAndId;

int get_building_id(int building_index) {
    int building_id;
    asm("mov eax, [%1];"
        "imul eax,0x32C;"
        "mov eax,[eax+0x0F9860C];"
        "mov [%0], eax;" : "=m"(building_id) : "m"(building_index));
    return building_id;
}

BuildingIndexAndId get_keep_building(int lord_id) {
    int building_id;
    int building_index;
    BuildingIndexAndId buildingIndexAndId;

    asm("mov eax, 0x39F4;"
        "mov ebx, [%1];"
        "imul eax, ebx;"

        "mov eax, [0x115be8c+eax];"
        "mov [%0], eax;": "=m"(building_index) : "m"(lord_id));

    building_id = get_building_id(building_index);

    buildingIndexAndId.index = building_index;
    buildingIndexAndId.id = building_id;

    return buildingIndexAndId;
}

typedef struct {
    int x;
    int y;
} Position;

Position get_building_position(int building_id) {
    int x, y;
    Position position;

    asm volatile ("imul ecx, ecx,0x000032C;"
        "movsx ebx,word ptr [ecx+0x0F98624];"
        "movsx eax,word ptr [ecx+0x0F98622];" : "=a"(x), "=b"(y) : "c"(building_id));

    position.x = x;
    position.y = y;

    return position;
}

int _count_goods(int lord_id, int good_base_address) {
    int good_count;
    lord_id--;
    asm("mov eax, 0x39F4;"
        "mov ebx, [%2];"
        "imul eax, ebx;"
        "mov ecx, [%1];"
        "mov eax, [ecx+eax];"
        "mov [%0], eax": "=m"(good_count) : "m"(good_base_address), "m"(lord_id));

    return good_count;
}

int count_golds(int lord_id) { return _count_goods(lord_id, 0x115FCF8); }

int count_woods(int lord_id) { return _count_goods(lord_id, 0x115FCC4); }

int count_hops(int lord_id) { return _count_goods(lord_id, 0x115FCC8); }

int count_stones(int lord_id) { return _count_goods(lord_id, 0x115FCCC); }

int count_irons(int lord_id) { return _count_goods(lord_id, 0x115FCD4); }

int count_pitches(int lord_id) { return _count_goods(lord_id, 0x115FCD8); }

int count_wheats(int lord_id) { return _count_goods(lord_id, 0x115FCE0); }

int count_ales(int lord_id) { return _count_goods(lord_id, 0x115FCF4); }

int count_flours(int lord_id) { return _count_goods(lord_id, 0x115FCFC); }

int count_breads(int lord_id) { return _count_goods(lord_id, 0x115FCE4); }

int count_cheeses(int lord_id) { return _count_goods(lord_id, 0x115FCE8); }

int count_meats(int lord_id) { return _count_goods(lord_id, 0x115FCEC); }

int count_apples(int lord_id) { return _count_goods(lord_id, 0x115FCF0); }

int count_bows(int lord_id) { return _count_goods(lord_id, 0x115FD00); }

int count_spears(int lord_id) { return _count_goods(lord_id, 0x115FD08); }

int count_maces(int lord_id) { return _count_goods(lord_id, 0x115FD10); }

int count_crossbows(int lord_id) { return _count_goods(lord_id, 0x115FD04); }

int count_pikes(int lord_id) { return _count_goods(lord_id, 0x115FD0C); }

int count_leather_armor(int lord_id) { return _count_goods(lord_id, 0x115FD18); }

int count_metal_armor(int lord_id) { return _count_goods(lord_id, 0x115FD1C); }

void set_tax(int lord_id, int tax) {
    asm("mov eax, [%0];"
        "imul eax,0x00039F4;"
        "mov ebx, [%1];"
        "mov [eax+0x115DF80], ebx;" : : "m"(lord_id), "m"(tax));
}

int get_tax(int lord_id) {
    int tax;
    asm("mov eax, [%1];"
        "imul eax,0x00039F4;"
        "add eax, 0x115DF80;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(tax): "m"(lord_id));
    return tax;
}

void set_rations(int lord_id, int rations) {
    lord_id--;
    asm("mov eax, [%0];"
        "imul eax,0x00039F4;"
        "mov ebx, [%1];"
        "mov [eax+0x1161978], ebx;" : : "m"(lord_id), "m"(rations));
}

int get_rations(int lord_id) {
    int rations;
    lord_id--;
    asm("mov eax, [%1];"
        "imul eax,0x00039F4;"
        "add eax, 0x1161978;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(rations): "m"(lord_id));
    return rations;
}

int is_lord_exist(int lord) {
    lord--;
    if ((*(int *)(0x191de14 + lord * 4) != -1) || (*(int *)(0x191de80 + lord * 4) != 0)) {
        return 1;
    }
    return 0;
}

int count_lords() {
    int i = 0;
    for (int j=1; j<=8; j++) {
        if (is_lord_exist(j)==1) {
            i++;
        }
    }
    return i;
}

int _get_last_unit() {
    return (*(int *)0x1387F38) - 1;
}

int count_units() {
    int j = 0;
    for (int i = 0; i<=_get_last_unit(); i++) {
        if (is_unit_exist(i)==1) {
            j++;
        }
    }
    return j;
}

typedef struct {
    int index;
    int id;
} UnitIndexAndId;

typedef struct {
    UnitIndexAndId unitIndexAndId[2500];
    int size;
} UnitIndexAndIdList;

UnitIndexAndIdList get_all_units() {
    UnitIndexAndIdList unitIndexAndIdList;
    int j = 0;
    for (int i = 0; i<=_get_last_unit(); i++) {
        if (is_unit_exist(i)==1) {
            unitIndexAndIdList.unitIndexAndId[j].index = i;
            unitIndexAndIdList.unitIndexAndId[j].id = get_unit_id(i);
            j++;
            unitIndexAndIdList.size = j;
        }
    }
    return unitIndexAndIdList;
}

int get_unit_type(int unit) {
    int unit_type;
    asm("mov eax, [%1];"
        "imul eax,0x490;"
        "add eax, 0x1388A6A;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(unit_type): "m"(unit));
    return unit_type;
}
int change_map_enabled;
char *map_path;

void change_map_path() {
    if (change_map_enabled==1) {
        memcpy((char*)0x123DAB7, map_path, 20);
    }
    // back to normal path 1
    asm ("leave;");
    // execute stole code
    asm ("mov ecx,ebx;");
    asm ("call 0x046C420;");
    // back to normal path 2
    asm ("jmp 0x0478729;");
}

void start_custom_skirmish(char* map, int lords_position[8]) {
    char *s2;
    s2 = (char*)malloc(20);
    memcpy(s2, map, 20);

    map_path = s2;
    change_map_enabled = 1;
    hook_at(0x0478722, (void*)change_map_path);
    asm("mov ebx, 0x0000001;"
        "mov esi, 0x05E82B8;"
        "push 0x2;"
        "call 0x04251A0;"
        "add esp,0x4;"

        "mov ebx, 0x0000001;"
        "mov esi, 0x05EC368;"
        "push 0x2;"
        "call 0x042BF00;"
        "add esp,0x4;");
    for (int i = 0; i<7; i++) {
        if (lords_position[i]!=-1) {
            asm("mov eax, 0x1A275D0;"
                "add eax, [%0];"
                "mov ebx, [%1];"
                "mov byte ptr [eax], bl;"

                "mov eax, [%0];"
                "imul eax, 0x4;"
                "add eax, 0x191DE14;"
                "mov dword ptr [eax], 0x0000001;"
                : : "m"(i), "m"(lords_position[i]));
        }
        else {
            asm("mov eax, 0x1A275D0;"
                "add eax, [%0];"
                "mov byte ptr [eax], 0xF6;"

                "mov eax, [%0];"
                "imul eax, 0x4;"
                "add eax, 0x191DE14;"
                "mov dword ptr [eax], 0xFFFFFFFF;"
                : : "m"(i));
        }
    }
//    free(s2);
}


void set_accessible_position_update_limit(char new_limit) {
    set_memory_permission(0x049961E, 1, PAGE_EXECUTE_READWRITE);
    unsigned char *limit = (unsigned char *)0x049961E;
    *limit = new_limit;
}

void _engineer_deselect() {
    if ((*(int *)0x13884B8 < (2*2) && *(int *)0x1fe7aec==190) || (*(int *)0x13884B8 < (3*2) && *(int *)0x1fe7aec==191)
        || (*(int *)0x13884B8 < (4*2) && *(int *)0x1fe7aec==192) || (*(int *)0x13884B8 < (5*2) && *(int *)0x1fe7aec==193)
        || (*(int *)0x13884B8 < (1*2) && *(int *)0x1fe7aec==194) || (*(int *)0x13884B8 < (2*2) && *(int *)0x1fe7aec==358)) {
        asm("mov dword ptr [0x1fe7aec], 0;");
    }
    asm("leave;"
        "jmp 0x0446131;");
}

void disable_engineer_deselect() {
    hook_at(0x044612b, (void*)_engineer_deselect);
    set_memory_permission(0x056537F, 1, PAGE_EXECUTE_READWRITE);
    set_memory_permission(0x056539D, 1, PAGE_EXECUTE_READWRITE);
    *(char *)0x056537F = 0x6;
    *(char *)0x056539D = 0x6;

}

int is_human_lord(int lord) {
    int is_human;
    asm("mov eax, [%1];"
        "imul eax, 4;"
        "add eax, 0x191DE10;"
        "mov eax, [eax];"
        "mov [%0], eax"
        : "=m"(is_human) : "m"(lord));
    if (is_human==1) {
        return 1;
    }
    return 0;
}


__attribute__ ((naked))
void disable_auto_place_stockpile_hook() {
    int lord;
    asm("mov %0, ebp": "=r"(lord) : );
    if (is_human_lord(lord)) {
        asm("add esp, 0x1C;"
            "jmp 0x0514dc7;");
    }
    else {
        asm("call 0x0508540;"
            "jmp 0x0514dc7;");
    }
}


void disable_auto_place_stockpile() {
    hook_at(0x0514dc2, (void*)disable_auto_place_stockpile_hook);
}

void disable_can_not_place_building_on_units() {
    set_memory_permission(0x04f9baa, 2, PAGE_EXECUTE_READWRITE);
    *(short *)0x04f9baa = 0x9090;
}

void show_image(const unsigned char *image, int width, int height, int x, int y) {
    asm("push [%0];"
        "push [%1];"
        "push [%2];"
        "push [%3];"
        "push [%4];"
        "mov ecx, 0x1FEA090;"
        "call 0x0454a60;": : "m"(image), "m"(width), "m"(height), "m"(y), "m"(x)
    );
    x = x + *(int *)0x21aec58;
    y = y + *(int *)0x21AEC5C;
    asm("push [%0];"
        "push [%1];"
        "push [%2];"
        "push [%3];"
        "push [%4];"
        "mov ecx, 0x1FEA090;"
        "call 0x044d3d0;": : "m"(image), "m"(width), "m"(height), "m"(y), "m"(x)
    );
//    0044d3d0 works only in game
//    00455390 doesn't work
//    0044fbf0 doesn't work
//    0044f170 Windows Error
//    00471890 access violation
//    00454a60 doesn't work in game
//    0044e630 access violation
//    00451e00  Windows Error
}


typedef struct {
    int x;
    int y;
} MousePosition;

MousePosition get_mouse_position() {
    MousePosition position;

    position.x = *(short *)0x0F2CBA4;
    position.y = *(short *)0x0F2CBA6;

    return position;
}


int is_mouse_clicked() {
    if (((*(int *)0x0f2c9d8)==1)) {
        return 1;
    }
    return 0;
}
typedef struct {
    int width;
    int height;
} Resolution;

Resolution get_resolution() {
    Resolution resolution;

    resolution.width = *(int *)0x0f98370;
    resolution.height = *(int *)0x0F98374;

    return resolution;
}

void disable_mouse_in_game() {
    *(int *)0x21AEBD8 = 0;
}

int is_game_created() {
    if ((*(int *)0x117CADC) == 0) {
        return 0;
    }
    return 1;
}

int has_market(int lord_id) {
    if (*(int *)(0x115bfa4 + lord_id * 0x39f4) != 0) {
        return 1;
    }
    return 0;
}

int get_my_lord() {
    return (*(int *)(0x1a275dc));
}

void buy(int number_of_goods, int good_id, int player_id) {
    int price;
    int golds;

    if (has_market(player_id) == 0) {
        return;
    }

    price = get_buying_price(player_id, good_id, number_of_goods);
    golds = count_golds(player_id);
    if (price < golds) {
        asm(// number of goods
            "push eax;"
            // good id
            "push ebx;"
            // player id
            "push ecx;"
            "mov ecx, 0x23FC8E8;"
            "call 0x04cc000;": : "a"(number_of_goods), "b"(good_id), "c"(player_id));
    }
}


void sell(int number_of_goods, int good_id, int player_id) {
    if (has_market(player_id) == 0) {
        return;
    }

    asm(// number of goods
        "push eax;"
        // good id
        "push ebx;"
        // player id
        "push ecx;"
        "mov ecx, 0x23FC8E8;"
        "call 0x04cbfa0;": : "a"(number_of_goods), "b"(good_id), "c"(player_id));
}

int _get_opened_menu() {
    return *(int *)0x1FE7D1C;
}

int is_custom_game_open() {
    if (_get_opened_menu() == 20) {
        return 1;
    }
    return 0;
}

int get_bot(int player_id) {
    int bot_id;
    player_id = player_id - 1;
    asm("mov eax, [%1];"
        "imul eax,0x4;"
        "add eax, 0x191DE80;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(bot_id): "m"(player_id));
    return bot_id;
}

#define MAX_NUMBER_OF_BOTS 16
int disabled_bots[MAX_NUMBER_OF_BOTS];
int num_disabled_bots = 0;

void disable_bot_hook() {
    int tick;

    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");
    asm ("push esi;");
    asm ("mov eax, [0x11BC680];"
        "mov [%0], eax;": "=m"(tick) :);
    if (tick < 9) {
        for (int i = 0; i < num_disabled_bots; i++) {
            asm ("mov eax, [0x11BC680];"
                "mov [%0], eax;": "=m"(tick) :);
            if (get_bot(tick) == disabled_bots[i]) {
                asm("mov eax, 0x1;"
                "add [0x11BC680], eax;");
                i = -1;
            }
        }
    }
    asm ("mov eax, [0x11bc684];"
            "mov [%0], eax;": "=m"(tick) :);
        if (tick < 9) {
            for (int i = 0; i < num_disabled_bots; i++) {
                asm ("mov eax, [0x11bc684];"
                    "mov [%0], eax;": "=m"(tick) :);
                if (get_bot(tick) == disabled_bots[i]) {
                    asm("mov eax, 0x1;"
                    "add [0x11bc684], eax;");
                    i = -1;
                }
            }
        }

    // restore registers
    asm ("pop esi;");
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");

    // back to normal path 1
    asm ("leave;");

    // execute stole code
    asm ("pop edi;"
         "pop esi;"
         "pop ebx;"
         "ret 0x008;");
}

void disable_bot(int bot_id) {
    if (num_disabled_bots == 0) {
        hook_at(0x045673c, (void*)disable_bot_hook);
    }
    disabled_bots[num_disabled_bots] = bot_id;
    num_disabled_bots++;
}

int _get_last_plant() {
    return (*(int *)0x0F2CC48) - 1;
}

int get_plant_id(int plant_index) {
    int plant_id;

    asm("mov eax, 0x9C;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov %0, [0x0F2CD3C+eax];" : "=r" (plant_id) : "m"(plant_index));
    return plant_id;
}

typedef struct {
    int index;
    int id;
} PlantIndexAndId;

typedef struct {
    PlantIndexAndId plantIndexAndId[2000];
    int size;
} PlantIndexAndIdList;

int is_plant_exist(int plant_index) {
    int exist;

    exist = get_plant_id(plant_index);

    if (exist!=0) {
        return 1;
    }
    return 0;
}

PlantIndexAndIdList get_all_plants() {
    PlantIndexAndIdList plantIndexAndIdList;
    int j = 0;
    for (int i = 0; i<=_get_last_plant(); i++) {
        if (is_plant_exist(i)==1) {
            plantIndexAndIdList.plantIndexAndId[j].index = i;
            plantIndexAndIdList.plantIndexAndId[j].id = get_plant_id(i);
            j++;
            plantIndexAndIdList.size = j;
        }
    }
    return plantIndexAndIdList;
}

int is_tree(int plant_index) {
    int is_tree;

    asm("mov eax, 0x9C;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov %0, dword ptr [0x0F2CD70+eax];" : "=r" (is_tree) : "m"(plant_index));
    if (is_tree==3) {
        return 1;
    }
    return 0;
}

Position get_plant_position(int plant_index) {
    int x, y;
    Position position;

    asm volatile ("imul ecx, ecx,0x9C;"
        "movsx ebx,word ptr [ecx+0x0F2CD54];"
        "movsx eax,word ptr [ecx+0x0F2CD52];" : "=a"(x), "=b"(y) : "c"(plant_index));

    position.x = x;
    position.y = y;

    return position;
}

int can_woodcutter_cut(int plant_index) {
    int can_woodcutter_cut;
    if (is_tree(plant_index)==1) {
        asm("mov eax, 0x9C;"
            "mov ebx, [%1];"
            "imul eax, ebx;"
            "mov %0, dword ptr [0x0F2CD68+eax];" : "=r" (can_woodcutter_cut) : "m"(plant_index));
        if (can_woodcutter_cut==0) {
            return 0;
        }
        return 1;
    }
    return 0;
}


int _get_last_building() {
    return (*(int *)0x0B95788) - 1;
}

typedef struct {
    BuildingIndexAndId buildingIndexAndId[2000];
    int size;
} BuildingIndexAndIdList;

int is_building_exist(int building_index) {
    int exist;

    exist = get_building_id(building_index);

    if (exist!=0) {
        return 1;
    }
    return 0;
}

BuildingIndexAndIdList get_all_buildings() {
    BuildingIndexAndIdList buildingIndexAndIdList;
    int j = 0;
    for (int i = 0; i<=_get_last_building(); i++) {
        if (is_building_exist(i)==1) {
            buildingIndexAndIdList.buildingIndexAndId[j].index = i;
            buildingIndexAndIdList.buildingIndexAndId[j].id = get_building_id(i);
            j++;
            buildingIndexAndIdList.size = j;
        }
    }
    return buildingIndexAndIdList;
}

char get_building_type(int building_index) {
    int building_type;

    asm("mov eax, 0x32C;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov eax, [0x0F98606+eax];"
        "mov [%0], eax;" : "=m" (building_type) : "m"(building_index));
    return building_type;
}

short get_building_owner(int building_index) {
    return *(short *)(0x0F9860A + building_index * 0x32C);
}

void show_text() {
    asm("mov eax, 0x0;"
        "mov [0x2157594], eax;"
        "mov ecx, 0x2157578;"
        "push 0x0;"
        "push 0x12;"
        "push 0x0;"
        "push 0x0B8EEFB;"
        "push 0x0;"
        "push 0xfa;"
        "push 0x190;"
        "push 0x80;"
        "push 0x8;"
        "call 0X0424390;"
        "mov eax, 0x0;"
        "mov [0x2157594],eax;"
        "mov eax, 0x1;"
        "mov [0x1FEA094],eax;");
}

void free_memory(char *ptr)
{
    free(ptr);
}

